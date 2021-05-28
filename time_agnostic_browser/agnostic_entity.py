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

from pprint import pprint
from typing import List, Tuple, Dict, Set
from datetime import datetime
from rdflib.graph import ConjunctiveGraph
from rdflib.term import URIRef
import copy
from rdflib.plugins.sparql.processor import processUpdate

from time_agnostic_browser.sparql import Sparql
from time_agnostic_browser.prov_entity import ProvEntity

class Agnostic_entity:
    def __init__(self, res:str, related_entities_history:bool=False):
        self.res = res
        self.related_entities_history = related_entities_history

    def get_history(self) -> Dict[str, Dict[str, ConjunctiveGraph]]:
        """
        Given the URI of a resource, it reconstructs its entire history, 
        returning a dictionary according to the following model:
        {
            "entity_URI": {
                "time_snapshot_1": graph_at_time_1,
                "time_snapshot_2": graph_at_time_2,
                "time_snapshot_n": graph_at_time_n
            }
        }
        What is meant by graph? By graph we mean all the triples that have 
        the entity as subject plus the provenance information present at time t 
        (not all existing ones, only those existing at that given instant).
        """
        if self.related_entities_history:
            entities_to_query = {self.res}
            current_state = self._query_dataset()
            related_entities = current_state.triples((None, None, URIRef(self.res)))
            for entity in related_entities:
                if ProvEntity.PROV not in entity[1]:
                    entities_to_query.add(str(entity[0]))
            return get_entities_histories(entities_to_query)
        entity_history = self._get_entity_current_state()
        entity_history = self._get_old_graphs(entity_history)
        return entity_history
    
    def get_state_at_time(self, time:str) -> Dict:
        entity_at_time = {time: None, "before": dict(), "after": dict()}
        entity_history = self.get_history()
        for snapshot in entity_history[self.res]:
            if self._convert_to_datetime(snapshot) < self._convert_to_datetime(time):
                entity_at_time["before"][snapshot] = entity_history[self.res][snapshot]
            elif self._convert_to_datetime(snapshot) > self._convert_to_datetime(time):
                entity_at_time["after"][snapshot] = entity_history[self.res][snapshot]
        entity_at_time[time] = entity_history[self.res][time]
        return entity_at_time
    
    def _get_entity_current_state(self) -> Dict[str, Dict[str, ConjunctiveGraph]]:
        """
        Given the URI of a resource, it outputs a dictionary populating only 
        the instant at time t, that is the present one, according to the following model:
        {
            "entity_URI": {
                "time_snapshot_1": graph_at_time_1,
                "time_snapshot_2": None,
                "time_snapshot_n": None
            }
        }        
        """
        entity_current_state = {self.res: dict()}
        current_state = ConjunctiveGraph()
        for quad in self._query_dataset().quads():
            current_state.add(quad)
        for quad in self._query_provenance().quads():
            current_state.add(quad)
        triples_generated_at_time = current_state.triples((None, ProvEntity.iri_generated_at_time, None))
        most_recent_time = None
        for triple in triples_generated_at_time:
            snapshot_time = triple[2]
            snapshot_date_time = self._convert_to_datetime(snapshot_time)
            if most_recent_time: 
                if snapshot_date_time > self._convert_to_datetime(most_recent_time):
                    most_recent_time = snapshot_time
            elif not most_recent_time:
                most_recent_time = snapshot_time
            entity_current_state[self.res][snapshot_time] = None
        entity_current_state[self.res][most_recent_time] = current_state
        return entity_current_state
    
    def _get_old_graphs(
        self, entity_current_state:Dict[str, Dict[str, ConjunctiveGraph]]
        ) -> Dict[str, Dict[str, ConjunctiveGraph]]:
        """
        Given as input the output of _get_entity_current_state, it populates the graphs 
        relating to the past snapshots of the resource.        
        """
        ordered_data:List[Tuple[str, ConjunctiveGraph]] = sorted(
            entity_current_state[self.res].items(), 
            key = lambda x:self._convert_to_datetime(x[0]), 
            reverse=True
            )
        for index, date_graph in enumerate(ordered_data):
            if index > 0:
                next_snapshot = ordered_data[index-1][0]
                previous_graph:ConjunctiveGraph = copy.deepcopy(entity_current_state[self.res][next_snapshot])
                snapshot_uri = list(previous_graph.subjects(object=next_snapshot))[0]
                snapshot_update_query:str = previous_graph.value(
                    subject=snapshot_uri, 
                    predicate=ProvEntity.iri_has_update_query,
                    object = None)
                snapshot_update_query = snapshot_update_query.replace("INSERT", "%temp%").replace("DELETE", "INSERT").replace("%temp%", "DELETE")
                processUpdate(previous_graph, snapshot_update_query)
                previous_graph.remove((snapshot_uri, None, None))
                entity_current_state[self.res][date_graph[0]] = previous_graph
        for time in list(entity_current_state[self.res]):
            entity_current_state[self.res][str(time)] = entity_current_state[self.res].pop(time)
        return entity_current_state
    
    def _query_dataset(self) -> ConjunctiveGraph:
        # A SELECT hack can be used to return RDF quads in named graphs, 
        # since the CONSTRUCT allows only to return triples in SPARQL 1.1.
        # Here is an exemple of SELECT hack:
        #
        # SELECT ?s ?p ?o ?c
        # WHERE {
        #     GRAPH ?c {?s ?p ?o}
        #     VALUES ?s {<{res}>}
        # }}
        #
        # Aftwerwards, the rdflib add method can be used to add quads to a Conjunctive Graph, 
        # where the fourth element is the context.    
        if self.related_entities_history:       
            query_dataset = f"""
                SELECT ?s ?p ?o ?c
                WHERE {{
                    GRAPH ?c {{?s ?p ?o}}
                    {{VALUES ?s {{<{self.res}>}}}}
                    UNION 
                    {{VALUES ?o {{<{self.res}>}}}}
                }}   
            """
        else:
            query_dataset = f"""
                SELECT ?s ?p ?o ?c
                WHERE {{
                    GRAPH ?c {{?s ?p ?o}}
                    VALUES ?s {{<{self.res}>}} 
                }}   
            """
        return Sparql().run_construct_query(query_dataset)
    
    def _query_provenance(self) -> ConjunctiveGraph:
        query_provenance = f"""
            CONSTRUCT {{
                ?snapshot <{ProvEntity.iri_generated_at_time}> ?t;      
                        <{ProvEntity.iri_has_update_query}> ?updateQuery.
            }} 
            WHERE {{
                ?snapshot <{ProvEntity.iri_specialization_of}> <{self.res}>;
                        <{ProvEntity.iri_generated_at_time}> ?t.
            OPTIONAL {{
                    ?snapshot <{ProvEntity.iri_has_update_query}> ?updateQuery.
                }}   
            }}
        """
        return Sparql().run_construct_query(query_provenance)
    
    @classmethod
    def _convert_to_datetime(cls, time_string:str) -> datetime:
        return datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S%z")

def get_entities_histories(res_set:Set[str], related_entities_history=False) -> Dict[str, Dict[str, ConjunctiveGraph]]:
    entities_histories = dict()
    for res in res_set:
        agnostic_entity = Agnostic_entity(res, related_entities_history)
        entities_histories.update(agnostic_entity.get_history())
    return entities_histories



    

