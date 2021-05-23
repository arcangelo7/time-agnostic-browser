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

import unittest, rdflib
from agnostic_query import Agnostic_query
from rdflib import Graph
from support import File_manager, Sparql
from SPARQLWrapper import JSON, XML

class Test_Agnostic_query(unittest.TestCase):
    def test_get_entity_current_state(self):
        input = "https://github.com/arcangelo7/time_agnostic/id/1"
        expected_output = {
            'https://github.com/arcangelo7/time_agnostic/id/1': {
                rdflib.term.Literal('2021-05-21T19:08:56+00:00', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#dateTime')): Graph(identifier="N50bb3c0e9338414c8d5f7363a8b6babf"), 
                rdflib.term.Literal('2021-05-14T17:07:03+00:00', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#dateTime')): None}}
        self.assertEqual(Agnostic_query.get_entity_current_state(input), expected_output)


class Test_File_manager(unittest.TestCase):
    def test_import_json(self):
        input = "./test/config.json"
        expected_output = {
            "triplestore_url": [
                "http://localhost:9999/blazegraph/sparql",
                "http://localhost:19999/blazegraph/sparql"
            ]
        }
        self.assertEqual(File_manager.import_json(input), expected_output)

class Test_Sparql(unittest.TestCase):
    def test_execute_query_JSON(self):
        input = """
            PREFIX pro: <http://www.w3.org/ns/prov#>
            SELECT ?s
            WHERE {
                ?s a pro:Entity.
                FILTER regex(str(?s), "se/2").
            }
        """
        expected_output = {'head': {'vars': ['s']}, 
        'results': {'bindings': 
            [{'s': {'type': 'uri', 'value': 'https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2'}}]
        }}
        self.assertEqual(Sparql("./test/config.json").execute_query(input, format=JSON), expected_output)

    def test_execute_query_XML(self):
        input = """
            CONSTRUCT {
                <https://github.com/arcangelo7/time_agnostic/br/1> ?p "1992"
            } 
            WHERE {
                <https://github.com/arcangelo7/time_agnostic/br/1> <http://prismstandard.org/namespaces/basic/2.0/publicationDate> ?o; 
                ?p ?o
            }
            """
        self.assertIsInstance(Sparql("./test/config.json").execute_query(input, format=XML), Graph)
    
if __name__ == '__main__':
    unittest.main()
