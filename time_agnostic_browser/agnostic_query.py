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

from rdflib.plugins.sparql.processor import prepareQuery
from rdflib.plugins.sparql.sparql import Query
from rdflib.plugins.sparql.parserutils import CompValue
from rdflib import ConjunctiveGraph, Literal
from tqdm import tqdm

from time_agnostic_browser.sparql import Sparql
from time_agnostic_browser.prov_entity import ProvEntity
from time_agnostic_browser.agnostic_entity import AgnosticEntity
from pprint import pprint


class AgnosticQuery:
    def __init__(self, query:str=""):
        self.query = query
        if query:
            prepare_query:Query = prepareQuery(self.query)
            algebra:CompValue = prepare_query.algebra
            if algebra.name != "SelectQuery":
                raise ValueError("Only SELECT queries are allowed")

    def run_the_sock(self):
        dict_of_snapshots = dict()
        query_times = f"""
            SELECT DISTINCT ?time
            WHERE {{
                ?snapshot <{ProvEntity.iri_generated_at_time}> ?time;
                    <{ProvEntity.iri_has_update_query}> ?updateQuery.
            }}
        """
        times = Sparql().run_select_query(query_times)
        for time in times:
            query_entities_at_time = f"""
                SELECT DISTINCT ?s
                WHERE {{
                    ?snapshot <{ProvEntity.iri_generated_at_time}> "{time[0]}"^^<http://www.w3.org/2001/XMLSchema#dateTime>;
                                <{ProvEntity.iri_has_update_query}> ?updateQuery;
                                <{ProvEntity.iri_specialization_of}> ?s.
                }}
            """
            entities_at_time = Sparql().run_select_query(query_entities_at_time)
            for entity_at_time in entities_at_time:
                dict_of_snapshots.setdefault(time[0], set())
                dict_of_snapshots[time[0]].add(entity_at_time[0])
        
        sock = dict()
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
            sock[snapshot] = graph_at_time
        pbar_snapshot.close()

        return sock

# results = AgnosticQuery().run_the_sock()
# for se, graph in results.items():
#     for quad in graph.quads():
#         pprint(quad)
    


