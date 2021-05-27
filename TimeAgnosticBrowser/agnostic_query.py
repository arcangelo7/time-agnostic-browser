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
from sparql import Sparql
from rdflib import ConjunctiveGraph


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

