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

from typing import Set, Tuple, Dict

import validators, json
from rdflib.plugins.sparql.processor import prepareQuery, evalQuery
from rdflib.plugins.sparql.sparql import Query
from rdflib.plugins.sparql.parserutils import CompValue
from rdflib import ConjunctiveGraph
from tqdm import tqdm

from time_agnostic_browser.support import FileManager
from time_agnostic_browser.sparql import Sparql
from time_agnostic_browser.prov_entity import ProvEntity
from time_agnostic_browser.agnostic_entity import AgnosticEntity
from pprint import pprint


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
        Depending on the amount of snapshots, reconstructing the past state of knowledge may take a long time. For example, reconstructing 26 different states in each of which 23,000 entities have changed takes about 12 hours. The experiment was performed with an Intel Core i5 8500, an Nvme Pcie 3.0 SSD and DDR4 3000 Mhz CL15 RAM. The amount of storage or RAM is unimportant, as only deltas are processed and the impact on both is minimal.
    """
    def __init__(self, past_graphs_location:str="", past_graphs_destination:str="past_graphs.json", query:str=""):
        self.query = query
        if not past_graphs_location:
            print("[AgnosticQuery: INFO] Recreating past graphs. That may take some considerable time.")
            self.past_graphs = self._rebuild_past_graphs()
            self._save_past_graphs(self.past_graphs, past_graphs_destination)
        else:
            self.past_graphs = FileManager(past_graphs_location).import_json()
        if query:
            prepare_query:Query = prepareQuery(self.query)
            algebra:CompValue = prepare_query.algebra
            if algebra.name != "SelectQuery":
                raise ValueError("Only SELECT queries are allowed")

    def _rebuild_past_graphs(self) -> Dict[str, ConjunctiveGraph]:
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
                for time, state in state_at_time.items():
                    graph_at_time += state
                pbar_state.update(1)
            pbar_state.close()
            pbar_snapshot.update(1)
            past_graphs[snapshot] = graph_at_time
        pbar_snapshot.close()
        return past_graphs

    def _save_past_graphs(self, past_graphs:Dict[str, ConjunctiveGraph], destination:str) -> None:
        if validators.url(destination):
            pass
        else:
            for snapshot, _ in past_graphs.items():
                cg_bytes = past_graphs[snapshot].serialize(format="json-ld")
                cg_string = cg_bytes.decode("utf8")
                cg_json = json.loads(cg_string)
                past_graphs[snapshot] = cg_json
            FileManager(path=destination).dump_json(past_graphs)
    
    def run_agnostic_query(self) -> Dict[str, Set[Tuple]]:
        agnostic_result = dict()
        present = Sparql().run_select_query(self.query)
        agnostic_result["now"] = present
        for snaphost, cg_json in self.past_graphs.items():
            cg = ConjunctiveGraph()
            cg.parse(data=json.dumps(cg_json), format="json-ld")
            results = cg.query(self.query)
            past = set()
            for result in results:
                result_tuple = tuple(str(var) for var in result)
                past.add(result_tuple)
            agnostic_result[snaphost] = past
        return agnostic_result

        

    


