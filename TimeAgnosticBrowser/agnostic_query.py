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

from typing import List, Tuple, Dict, Set

from datetime import datetime
from rdflib.graph import ConjunctiveGraph
from rdflib.term import URIRef
from sparql import Sparql
from prov_entity import ProvEntity
import copy, validators
from rdflib.plugins.sparql.processor import processUpdate
from rdflib.plugins.sparql.processor import prepareQuery
from rdflib.plugins.sparql.sparql import Query
from rdflib.plugins.sparql.parserutils import CompValue


class Agnostic_query:
    def __init__(self, query:str):
        self.query = query
        prepare_query:Query = prepareQuery(self.query)
        algebra:CompValue = prepare_query.algebra
        if algebra.name != "SelectQuery":
            raise ValueError("Only SELECT queries are allowed")
    
    def run_agnostic_query(self, base_uri:str, related_entities_history:bool=False) -> Tuple[Set[Tuple], Dict[str, Dict[str, ConjunctiveGraph]]]:
        user_query_results = Sparql().run_select_query(self.query)
        entities = set()
        for result in user_query_results:
            for x in result:
                if base_uri in x:
                    entities.add(str(x))
        entities_histories = self.get_entities_histories(entities, related_entities_history)
        return user_query_results, entities_histories
    
    @classmethod
    def get_entities_histories(cls, res_set:set, related_entities_history:bool=False) -> Dict[str, Dict[str, ConjunctiveGraph]]:
        entities_histories = dict()
        for res in res_set:
            entities_histories.update(cls.get_entity_history(res, related_entities_history))
        return entities_histories

    @classmethod
    def get_entity_history(cls, res:str, related_entities_history:bool=False) -> Dict[str, Dict[str, ConjunctiveGraph]]:
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
        if related_entities_history:
            entities_to_query = {res}
            current_state = cls._query_dataset(res, related_entities_history)
            related_entities = current_state.triples((None, None, URIRef(res)))
            for entity in related_entities:
                if ProvEntity.PROV not in entity[1]:
                    entities_to_query.add(str(entity[0]))
            return cls.get_entities_histories(entities_to_query)
        entity_history = cls._get_entity_current_state(res)
        entity_history = cls._get_old_graphs(entity_history, res)
        return entity_history
    
    @classmethod
    def _get_entity_current_state(cls, res:str) -> Dict[str, Dict[str, ConjunctiveGraph]]:
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
        entity_current_state = {res: dict()}
        current_state = ConjunctiveGraph()
        for quad in cls._query_dataset(res).quads():
            current_state.add(quad)
        for quad in cls._query_provenance(res).quads():
            current_state.add(quad)
        triples_generated_at_time = current_state.triples((None, ProvEntity.iri_generated_at_time, None))
        most_recent_time = None
        for triple in triples_generated_at_time:
            snapshot_time = triple[2]
            snapshot_date_time = cls._convert_to_datetime(snapshot_time)
            if most_recent_time: 
                if snapshot_date_time > cls._convert_to_datetime(most_recent_time):
                    most_recent_time = snapshot_time
            elif not most_recent_time:
                most_recent_time = snapshot_time
            entity_current_state[res][snapshot_time] = None
        entity_current_state[res][most_recent_time] = current_state
        return entity_current_state
    
    @classmethod
    def _get_old_graphs(
        cls, entity_current_state:Dict[str, Dict[str, ConjunctiveGraph]], res:str
        ) -> Dict[str, Dict[str, ConjunctiveGraph]]:
        """
        Given as input the output of _get_entity_current_state, it populates the graphs 
        relating to the past snapshots of the resource.        
        """
        ordered_data:List[Tuple[str, ConjunctiveGraph]] = sorted(
            entity_current_state[res].items(), 
            key = lambda x:cls._convert_to_datetime(x[0]), 
            reverse=True
            )
        for index, date_graph in enumerate(ordered_data):
            if index > 0:
                next_snapshot = ordered_data[index-1][0]
                previous_graph:ConjunctiveGraph = copy.deepcopy(entity_current_state[res][next_snapshot])
                snapshot_uri = list(previous_graph.subjects(object=next_snapshot))[0]
                snapshot_update_query:str = previous_graph.value(
                    subject=snapshot_uri, 
                    predicate=ProvEntity.iri_has_update_query,
                    object = None)
                snapshot_update_query = snapshot_update_query.replace("INSERT", "%temp%").replace("DELETE", "INSERT").replace("%temp%", "DELETE")
                processUpdate(previous_graph, snapshot_update_query)
                previous_graph.remove((snapshot_uri, None, None))
                entity_current_state[res][date_graph[0]] = previous_graph
        for time in list(entity_current_state[res]):
            entity_current_state[res][str(time)] = entity_current_state[res].pop(time)
        return entity_current_state
    
    @classmethod
    def _query_dataset(cls, res:str, related_entities_history:bool=False) -> ConjunctiveGraph:
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
        if related_entities_history:       
            query_dataset = f"""
                SELECT ?s ?p ?o ?c
                WHERE {{
                    GRAPH ?c {{?s ?p ?o}}
                    {{VALUES ?s {{<{res}>}}}}
                    UNION 
                    {{VALUES ?o {{<{res}>}}}}
                }}   
            """
        else:
            query_dataset = f"""
                SELECT ?s ?p ?o ?c
                WHERE {{
                    GRAPH ?c {{?s ?p ?o}}
                    VALUES ?s {{<{res}>}} 
                }}   
            """
        return Sparql().run_construct_query(query_dataset)
    
    @classmethod
    def _query_provenance(cls, res) -> ConjunctiveGraph:
        query_provenance = f"""
            CONSTRUCT {{
                ?snapshot <{ProvEntity.iri_generated_at_time}> ?t;      
                        <{ProvEntity.iri_has_update_query}> ?updateQuery.
            }} 
            WHERE {{
                ?snapshot <{ProvEntity.iri_specialization_of}> <{res}>;
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



    


