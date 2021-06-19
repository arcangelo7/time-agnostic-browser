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
from rdflib.plugins.sparql.parser import Var

import warnings
from rdflib.plugins.sparql.processor import prepareQuery
from rdflib.plugins.sparql.sparql import Query
from rdflib.plugins.sparql.parserutils import CompValue
from rdflib import ConjunctiveGraph, URIRef, Literal, Variable
from tqdm import tqdm
from datetime import datetime
from dateutil import parser

from time_agnostic_browser.support import FileManager, _to_nt_sorted_list, _to_dict_of_nt_sorted_lists
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
        Depending on the amount of snapshots, reconstructing the past state of knowledge may take a long time. For example, reconstructing 26 different states in each of which 23,000 entities have changed takes about 12 hours. The experiment was performed with an Intel Core i5 8500, a 1 TB SSD Nvme Pcie 3.0, and 32 GB RAM DDR4 3000 Mhz CL15.
    """
    def __init__(self, query:str):
        self.query = query
        self.complex_query = False
        self.triples = self._process_query()
        self.relevant_graphs = self._rebuild_relevant_graphs()
    
    def _tree_traverse(self, tree:dict, key:str, values:list) -> None:
        for k, v in tree.items():
            if k == key:
                values.extend(v)
            elif isinstance(v, dict):
                found = self._tree_traverse(v, key, values)
                if found is not None:  
                    values.extend(found)
    
    def _process_query(self) -> list:
        algebra:CompValue = prepareQuery(self.query).algebra
        if algebra.name != "SelectQuery":
            raise ValueError("Only SELECT queries are allowed.")
        triples_dict = algebra["p"]["p"]["p"]
        triples = list()
        # The structure of the triples_dict dictionary can be extremely variable 
        # in case of one or more OPTIONAL in the query: it is necessary to navigate   
        # the dictionary recursively in search of the values of the "triples" keys.
        self._tree_traverse(triples_dict, "triples", triples)
        triples_with_hook = [triple for triple in triples if isinstance(triple[0], URIRef) or isinstance(triple[2], URIRef)]
        if not triples_with_hook:
            raise ValueError("Could not perform a generic time agnostic query. Please, specify at least one entity within the query.")
        easy_triples = [triple for triple in triples_with_hook if isinstance(triple[0], URIRef)]
        if not easy_triples:
            warnings.warn("If the query contains only explicit objects it will take more time. To speed up the query, specify at least one subject.")
            self.complex_query = True
        return triples
    
    def _rebuild_relevant_entity(self, entity:str, reconstructed_entities:set, relevant_entities_graphs:dict):
        if isinstance(entity, URIRef) and entity not in reconstructed_entities:
            agnostic_entity = AgnosticEntity(entity, self.complex_query)
            entity_history = agnostic_entity.get_history()
            if entity_history[entity]:
                relevant_entities_graphs.update(entity_history) 
            reconstructed_entities.add(entity)
    
    def _align_snapshots(self, relevant_entities_graphs:Dict[str, Dict[str, ConjunctiveGraph]]) -> Dict[str, ConjunctiveGraph]:
        relevant_graphs:Dict[str, ConjunctiveGraph] = dict()
        # Merge entities based on snapshots
        for _, snapshots in relevant_entities_graphs.items():
            for snapshot, relevant_graph in snapshots.items():
                if snapshot in relevant_graphs:
                    for quad in relevant_graph.quads():
                        relevant_graphs[snapshot].add(quad)
                else:
                    relevant_graphs[snapshot] = relevant_graph
        # If an entity hasn't changed, copy it
        ordered_data: List[Tuple[str, ConjunctiveGraph]] = sorted(
            relevant_graphs.items(),
            key=lambda x: parser.parse(x[0]),
            reverse=False
        )
        for index, se_cg in enumerate(ordered_data):
            if index > 0:
                previous_se = ordered_data[index-1][0]
                for subject in relevant_graphs[previous_se].subjects():
                    if (subject, None, None, None) not in se_cg[1]:
                        for quad in relevant_graphs[previous_se].quads((subject, None, None, None)):
                            relevant_graphs[se_cg[0]].add(quad)
        return relevant_graphs
    
    def _rebuild_relevant_graphs(self) -> Dict[str, ConjunctiveGraph]:
        reconstructed_entities = set()
        relevant_entities_graphs:Dict[str, Dict[str, ConjunctiveGraph]] = dict()
        # First, the graphs of the hooks are reconstructed
        for triple in self.triples:
            self._rebuild_relevant_entity(triple[0], reconstructed_entities, relevant_entities_graphs)
            self._rebuild_relevant_entity(triple[2], reconstructed_entities, relevant_entities_graphs)
        relevant_graphs = self._align_snapshots(relevant_entities_graphs)
        # Then, the graphs of the entities obtained from the hooks are reconstructed
        self._explicit_query(relevant_graphs, reconstructed_entities, relevant_entities_graphs)
        return relevant_graphs
        
    def _explicit_query(self, relevant_graphs:Dict[str, ConjunctiveGraph], reconstructed_entities:set, relevant_entities_graphs:dict) -> str:
        triples_to_explicit = {triple for triple in self.triples if isinstance(triple[0], Variable) or isinstance(triple[2], Variable)}
        triples_to_explicit_by_time:Dict[str, Dict[str, List]] = dict()
        for se, _ in relevant_graphs.items():
            triples_to_explicit_by_time[se] = dict()
            for triple in self.triples:
                variables = [el for el in triple if isinstance(el, Variable)]
                for variable in variables:
                    triples_to_explicit_by_time[se].setdefault(variable, list()) 
                    triples_to_explicit_by_time[se][variable].append(triple)
        runs = len(triples_to_explicit)
        while runs:
            explicit_triples:Dict[str, Dict[str, str]] = dict()
            for se, vars in triples_to_explicit_by_time.items():
                for var, triples in vars.items():
                    for triple in triples:
                        solvable_triple = [f"<{el}>" if isinstance(el, URIRef) else f"?{el}" if isinstance(el, Variable) else el for el in triple]
                        variables = [x for x in solvable_triple if x.startswith("?")]
                        if len(variables) == 1:
                            variable = variables[0]
                            variable_index = solvable_triple.index(variable)
                            query_to_identify = f"""
                                CONSTRUCT {{{solvable_triple[0]} {solvable_triple[1]} {solvable_triple[2]}}}
                                WHERE {{{solvable_triple[0]} {solvable_triple[1]} {solvable_triple[2]}}}
                            """
                            results = relevant_graphs[se].query(query_to_identify)
                            for result in results:
                                explicit_var = result[variable_index]
                                explicit_triples.setdefault(se, dict())
                                explicit_triples[se][var] = explicit_var
                                self._rebuild_relevant_entity(explicit_var, reconstructed_entities, relevant_entities_graphs)
                            relevant_graphs = self._align_snapshots(relevant_entities_graphs)
            if not explicit_triples:
                return 
            for se, vars in triples_to_explicit_by_time.items():
                for var, triples in vars.items():
                    for triple in triples:
                        for explicit_var, explicit_el in explicit_triples[se].items():
                            new_triple = tuple(explicit_el if el == explicit_var else el for el in triple)
                            new_list_of_triples = [new_triple if x == triple else x for x in triples_to_explicit_by_time[se][var]]
                            triples_to_explicit_by_time[se][var] = new_list_of_triples              
            runs -= 1
        
    def run_agnostic_query(self) -> Dict[str, Set[Tuple]]:
        """
        It launches a time agnostic query, 
        which returns the result not only with respect to the current state of knowledge, 
        but also with respect to past ones.

        :returns Dict[str, Set[Tuple]] -- A dictionary is returned in which the keys correspond to the recorded snapshots, while the values correspond to a set of tuples containing the query results at that snapshot, where the positional value of the elements in the tuples is equivalent to the order of the variables indicated in the query.
        """
        agnostic_result = dict()
        for snapshot, graph in self.relevant_graphs.items():
            results = graph.query(self.query)
            output = set()
            for result in results:
                result_tuple = tuple(str(var) for var in result)
                output.add(result_tuple)
            agnostic_result[snapshot] = output
        return agnostic_result

        

    


