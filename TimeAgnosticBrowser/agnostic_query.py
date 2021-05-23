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

from typing import List, Tuple, Dict
from datetime import datetime

from rdflib.graph import Graph
from sparql import Sparql
from SPARQLWrapper import XML, JSON
from prov_entity import ProvEntity
import copy
from rdflib.plugins.sparql.processor import processUpdate
from pprint import pprint

class Agnostic_query:
    def __init__(self, query=""):
        self.query = query
        self.entities_provenance = dict()

    @classmethod
    def get_entity_history(cls, res:str) -> Dict[str, Dict[str, Graph]]:
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
        entity_history = cls._get_entity_current_state(res)
        entity_history = cls._get_old_graphs(entity_history, res)
        return entity_history

    @classmethod
    def _get_entity_current_state(cls, res:str) -> Dict[str, Dict[str, Graph]]:
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
        query = f"""
            CONSTRUCT {{
                <{res}> ?p ?o. 
                ?snapshot <{ProvEntity.iri_generated_at_time}> ?t;      
                        <{ProvEntity.iri_has_update_query}> ?updateQuery.
            }}
            WHERE {{
                ?snapshot <{ProvEntity.iri_specialization_of}> <{res}>;
                        <{ProvEntity.iri_generated_at_time}> ?t.
                OPTIONAL {{
                    <{res}> ?p ?o.
                }}     
                OPTIONAL {{
                    ?snapshot <{ProvEntity.iri_has_update_query}> ?updateQuery.
                }}   
            }}   
        """
        current_state = Sparql().execute_query(query=query, format=XML)
        triples_generated_at_time = current_state.triples((None, ProvEntity.iri_generated_at_time, None))
        most_recent_time = None
        for triple in triples_generated_at_time:
            snapshot_time = triple[2]
            snapshot_date_time = datetime.strptime(snapshot_time, "%Y-%m-%dT%H:%M:%S%z")
            if most_recent_time: 
                if snapshot_date_time > datetime.strptime(most_recent_time, "%Y-%m-%dT%H:%M:%S%z"):
                    most_recent_time = snapshot_time
            elif not most_recent_time:
                most_recent_time = snapshot_time
            entity_current_state[res][snapshot_time] = None
        entity_current_state[res][most_recent_time] = current_state
        return entity_current_state
    
    @classmethod
    def _get_old_graphs(
        cls, entity_current_state:Dict[str, Dict[str, Graph]], res:str
        ) -> Dict[str, Dict[str, Graph]]:
        """
        Given as input the output of _get_entity_current_state, it populates the graphs 
        relating to the past snapshots of the resource.        
        """
        ordered_data:List[Tuple[str, Graph]] = sorted(
            entity_current_state[res].items(), 
            key = lambda x:datetime.strptime(x[0], "%Y-%m-%dT%H:%M:%S%z"), 
            reverse=True
            )
        for index, date_graph in enumerate(ordered_data):
            if index > 0:
                previous_snapshot = ordered_data[index-1][0]
                previous_graph:Graph = copy.deepcopy(entity_current_state[res][previous_snapshot])
                snapshot_uri = list(previous_graph.subjects(object=previous_snapshot))[0]
                snapshot_update_query:str = previous_graph.value(
                    subject=snapshot_uri, 
                    predicate=ProvEntity.iri_has_update_query,
                    object = None)
                snapshot_update_query = snapshot_update_query.replace("INSERT", "%temp%").replace("DELETE", "INSERT").replace("%temp%", "DELETE")
                previous_graph.update(snapshot_update_query)
                previous_graph.remove((snapshot_uri, None, None))
                entity_current_state[res][date_graph[0]] = previous_graph
        return entity_current_state

    


