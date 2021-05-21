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

from datetime import datetime
from support import Sparql
from SPARQLWrapper import XML, JSON
from prov_entity import ProvEntity
from rdflib.plugins.sparql.processor import SPARQLUpdateProcessor

class Agnostic_query:
    def __init__(self, query=""):
        self.query = query
        self.entities_provenance = dict()

    @classmethod
    def get_entity_history(cls, res:str) -> dict:
        entity_cur_state = {res: dict()}
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
        current_state = Sparql()._execute_query(query=query, format=XML)
        triples_generated_at_time = current_state.triples((None, ProvEntity.iri_generated_at_time, None))
        replacement_rules = {"INSERT": "DELETE", "DELETE": "INSERT"}
        for triple in triples_generated_at_time:
            snapshot_time = triple[2]
            snapshot_uri = list(current_state.subjects(object=snapshot_time))[0]
            snapshot_update_query = list(current_state.objects(subject=snapshot_uri, predicate=ProvEntity.iri_has_update_query))
            if snapshot_update_query:
                snapshot_update_query = snapshot_update_query[0]
                for i, j in replacement_rules.items():
                    snapshot_update_query = snapshot_update_query.replace(i, j)
                # current_state.update(snapshot_update_query)
            entity_cur_state[res].setdefault(snapshot_time, current_state)
        return entity_cur_state
    


