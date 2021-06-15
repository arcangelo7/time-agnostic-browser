#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2021, Arcangelo Massari <arcangelomas@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.

from typing import Set, Tuple, Dict, List
from SPARQLWrapper.Wrapper import SPARQLWrapper, POST, JSON

import validators, json, re
from rdflib.plugins.sparql.processor import prepareQuery
from rdflib.plugins.sparql.sparql import Query
from rdflib.plugins.sparql.parserutils import CompValue
from rdflib import ConjunctiveGraph, URIRef, Literal
from tqdm import tqdm
from datetime import datetime
from dateutil import parser

from time_agnostic_browser.support import FileManager
from time_agnostic_browser.sparql import Sparql
from time_agnostic_browser.prov_entity import ProvEntity
from time_agnostic_browser.agnostic_entity import AgnosticEntity


class AgnosticQuery:
    """
    This class represents a time agnostic query, that is, it is executed both on the present state of knowledge and on those passed.

    :param past_graphs_location: Path of a file or URL of a triplestore from which to derive the past graphs. If nothing is indicated, the graphs are automatically reconstructed to the destination indicated in the parameter "past_graphs_destination".
    :type past_graphs_location: str
    :param past_graphs_destination: Destination to save past graphs to. You can specify both a path or the URL of a triplestore. If nothing is indicated, by default it is a file named "past_graphs.json" in the current directory.
    :type past_graphs_destination: str
    :param query: The query to execute on all the present and passed states of all the graphs.
    :type query: str

    .. CAUTION::
        Depending on the amount of snapshots, reconstructing the past state of knowledge may take a long time. For example, reconstructing 26 different states in each of which 23,000 entities have changed takes about 12 hours. The experiment was performed with an Intel Core i5 8500, a 1 TB SSD Nvme Pcie 3.0, and 32 GB RAM DDR4 3000 Mhz CL15.
    """
    def __init__(self, past_graphs_location:str="", past_graphs_destination:str="past_graphs.json", query:str=""):
        self.past_graphs_location = past_graphs_location
        self.query = query
        if not past_graphs_location:
            print("[AgnosticQuery: INFO] Recreating past graphs. That may take some considerable time.")
            past_graphs = self._rebuild_past_graphs()
            self._save_past_graphs(past_graphs, past_graphs_destination)
            self.past_graphs_location = past_graphs_destination
        if query:
            prepare_query:Query = prepareQuery(self.query)
            algebra:CompValue = prepare_query.algebra
            self.vars_list = algebra["PV"]
            if algebra.name != "SelectQuery":
                raise ValueError("Only SELECT queries are allowed")
    
    def _rebuild_past_graphs(self):
        deltas = self._rebuild_deltas()
        past_graphs = self._complete_past_graphs(deltas)
        return past_graphs
    
    def _rebuild_deltas(self) -> Dict[str, ConjunctiveGraph]:
        dict_of_snapshots:Dict[str, Set] = dict()
        query_times = f"""
            SELECT DISTINCT ?time
            WHERE {{
                ?snapshot <{ProvEntity.iri_generated_at_time}> ?future;
                    <{ProvEntity.iri_was_derived_from}> ?other_snapshot.
                ?other_snapshot <{ProvEntity.iri_generated_at_time}> ?time.
            }}
        """
        times = Sparql().run_select_query(query_times)
        for time in times:
            query_entities_at_time = f"""
                SELECT DISTINCT ?s
                WHERE {{
                    ?snapshot <{ProvEntity.iri_generated_at_time}> "{time[0]}"^^<http://www.w3.org/2001/XMLSchema#dateTime>;
                            <{ProvEntity.iri_specialization_of}> ?s.
                    ?other_snapshot <{ProvEntity.iri_was_derived_from}> ?snapshot.
                }}
            """
            entities_at_time = Sparql().run_select_query(query_entities_at_time)
            for entity_at_time in entities_at_time:
                dict_of_snapshots.setdefault(time[0], set())
                dict_of_snapshots[time[0]].add(entity_at_time[0])        
        past_graphs = dict()
        pbar_snapshot = tqdm(total=len(dict_of_snapshots))
        for snapshot, set_of_entities in dict_of_snapshots.items():
            graph_at_time = ConjunctiveGraph()
            pbar_state = tqdm(total=len(set_of_entities))
            for entity in set_of_entities:
                agnostic_entity = AgnosticEntity(res=entity, related_entities_history=False)
                state_at_time = agnostic_entity.get_state_at_time(time=snapshot, get_hooks=False)
                graph_at_time += state_at_time[0]
                pbar_state.update(1)
            pbar_state.close()
            pbar_snapshot.update(1)
            past_graphs[snapshot] = graph_at_time
        pbar_snapshot.close()
        return past_graphs
    
    def _complete_past_graphs(self, deltas:Dict[str, ConjunctiveGraph]):
        ordered_data: List[Tuple[str, ConjunctiveGraph]] = sorted(
            deltas.items(),
            key=lambda x: parser.parse(x[0], ignoretz=True),
            reverse=True
        )
        query_cur_graphs = f"""
            SELECT DISTINCT ?s ?p ?o ?c
            WHERE {{
                GRAPH ?c {{?s ?p ?o}}
                FILTER NOT EXISTS {{ ?s a <{ProvEntity.iri_entity}>. }}
            }}
        """
        cur_graphs = Sparql().run_construct_query(query_cur_graphs)
        complete_past_graphs:Dict[str, ConjunctiveGraph] = dict()
        for index, snapshot_cg in enumerate(ordered_data):
            snapshot = snapshot_cg[0]
            cg = snapshot_cg[1]
            complete_past_graph = ConjunctiveGraph(identifier=f"https://time_agnostic_browser/{snapshot}")
            complete_past_graph.add((URIRef(f"https://time_agnostic_browser/{snapshot}"), URIRef("http://purl.org/dc/terms/date"), Literal(snapshot)))
            if index > 0:
                future_snapshot = ordered_data[index-1][0]
                future_cg = deltas[future_snapshot]
                for subject in cg.subjects():
                    future_cg.remove((subject, None, None))
                complete_past_graph += future_cg + cg
            else:
                for subject in cg.subjects():
                    cur_graphs.remove((subject, None, None))
                complete_past_graph += cur_graphs + cg
            complete_past_graphs[snapshot] = complete_past_graph
        return complete_past_graphs

    def _save_past_graphs(self, past_graphs:Dict[str, ConjunctiveGraph], destination:str) -> None:
        if validators.url(destination):
            for snapshot, cg in past_graphs.items():
                query_string = f"INSERT DATA {{ GRAPH <https://time_agnostic_browser/{snapshot}> {{"
                for triple in cg.triples((None, None, None)):
                    if validators.url(triple[2]):
                        query_string += f"<{triple[0]}><{triple[1]}><{triple[2]}>."
                    else:
                        try:
                            float(triple[2])
                            query_string += f"<{triple[0]}><{triple[1]}>{triple[2]}."
                        except ValueError:
                            obj = triple[2].replace('\n', '').replace("'", '"')
                            query_string += f"<{triple[0]}><{triple[1]}>'{obj}'."
                query_string += f"}}}}; INSERT DATA {{<https://time_agnostic_browser/{snapshot}><http://purl.org/dc/terms/date>'{snapshot}'.}}"
                sparql = SPARQLWrapper(destination)
                sparql.setMethod(POST)
                sparql.setQuery(query_string)
                sparql.query()
        else:
            sum_of_cgs = ConjunctiveGraph()            
            for _, cg in past_graphs.items():
                for quad in cg.quads():
                    sum_of_cgs.add(quad)
            cg_bytes = sum_of_cgs.serialize(format="json-ld")
            cg_string = cg_bytes.decode("utf8")
            cg_json = json.loads(cg_string)
            FileManager(path=destination).dump_json(cg_json)
    
    def run_agnostic_query(self) -> Dict[str, Set[Tuple]]:
        """
        It launches a time agnostic query, 
        which returns the result not only with respect to the current state of knowledge, 
        but also with respect to past ones.

        :returns Dict[str, Set[Tuple]] -- A dictionary is returned in which the keys correspond to the recorded snapshots, while the values correspond to a set of tuples containing the query results at that snapshot, where the positional value of the elements in the tuples is equivalent to the order of the variables indicated in the query.
        """
        agnostic_result = dict()
        present = Sparql().run_select_query(self.query)
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        agnostic_result[now] = present
        if validators.url(self.past_graphs_location):
            agnostic_result.update(self._query_agnostic_triplestore())
        else:
            agnostic_result.update(self._query_agnostic_file())
        return agnostic_result

    def _query_agnostic_triplestore(self):
        agnostic_result = dict()
        query_other_dates = """
            SELECT DISTINCT ?g ?date
            WHERE {
                GRAPH ?g {?s ?p ?o}
                ?g <http://purl.org/dc/terms/date> ?date.
            }
        """
        split_query = re.split("WHERE", self.query, re.IGNORECASE)
        sparql = SPARQLWrapper(self.past_graphs_location)
        sparql.setMethod(POST)
        sparql.setQuery(query_other_dates)
        sparql.setReturnFormat(JSON)
        other_dates = sparql.queryAndConvert()
        for g in other_dates["results"]["bindings"]:
            agnositc_query = split_query[0] + f"FROM <{g['g']['value']}> WHERE" + split_query[1]
            sparql.setQuery(agnositc_query)
            results = sparql.queryAndConvert()
            output = set()
            for result_dict in results["results"]["bindings"]:
                results_list = list()
                for var in self.vars_list:
                    if str(var) in result_dict:
                        results_list.append(result_dict[str(var)]["value"])
                    else:
                        results_list.append(None)
                output.add(tuple(results_list))
            agnostic_result[g['date']['value']] = output
        return agnostic_result

    def _query_agnostic_file(self):
        agnostic_result = dict()
        past_graphs = ConjunctiveGraph()
        past_graphs.parse(location=self.past_graphs_location, format="json-ld")
        contexts = past_graphs.contexts()
        for context in contexts:
            date = list(context.objects(subject=URIRef(context.identifier), predicate=URIRef("http://purl.org/dc/terms/date")))[0]
            results = context.query(self.query)
            output = set()
            for result in results:
                result_tuple = tuple(str(var) for var in result)
                output.add(result_tuple)
            agnostic_result[str(date)] = output
        return agnostic_result
    
        

    


