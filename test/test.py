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

import unittest, datetime, rdflib

from rdflib.graph import ConjunctiveGraph
from rdflib import Literal, URIRef
from SPARQLWrapper import JSON, XML
from pprint import pprint
from dateutil.tz import tzutc

from time_agnostic_browser.sparql import Sparql
from time_agnostic_browser.prov_entity import ProvEntity
from time_agnostic_browser.agnostic_entity import AgnosticEntity
from time_agnostic_browser.support import FileManager, _to_dict_of_nt_sorted_lists, _to_nt_sorted_list

class Test_AgnosticEntity(unittest.TestCase):
    def test_get_history(self):
        input = "https://github.com/arcangelo7/time_agnostic/id/1"
        output = _to_dict_of_nt_sorted_lists(AgnosticEntity(input).get_history())
        expected_output = {
            'https://github.com/arcangelo7/time_agnostic/id/1': {
                datetime.datetime(2021, 6, 4, 11, 15, 32, tzinfo=tzutc()): [
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028089"', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>'], 
                datetime.datetime(2021, 6, 4, 9, 36, 53, tzinfo=tzutc()): [
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028088"^^<http://www.w3.org/2001/XMLSchema#string>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>'], 
                datetime.datetime(2021, 5, 29, 16, 20, 22, tzinfo=tzutc()): [
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028087"^^<http://www.w3.org/2001/XMLSchema#string>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028088"^^<http://www.w3.org/2001/XMLSchema#string>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>'
                ]
            }
        }      
        self.assertEqual(output, expected_output)
    
    def test_get_history_and_related_entities(self):
        input = "https://github.com/arcangelo7/time_agnostic/id/2"
        output = _to_dict_of_nt_sorted_lists(AgnosticEntity(input, related_entities_history=True).get_history())
        expected_output = {
            'https://github.com/arcangelo7/time_agnostic/id/2': {
                datetime.datetime(2021, 5, 29, 16, 20, 22, tzinfo=tzutc()): [
                    '<https://github.com/arcangelo7/time_agnostic/id/2> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/issn>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/2> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "0138-9130"', 
                    '<https://github.com/arcangelo7/time_agnostic/id/2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>'
                ]
            }, 
            'https://github.com/arcangelo7/time_agnostic/ra/2': {
                datetime.datetime(2021, 5, 29, 16, 20, 22, tzinfo=tzutc()): [
                    '<https://github.com/arcangelo7/time_agnostic/ra/2> <http://purl.org/spar/datacite/hasIdentifier> <https://github.com/arcangelo7/time_agnostic/id/2>', 
                    '<https://github.com/arcangelo7/time_agnostic/ra/2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Agent>', 
                    '<https://github.com/arcangelo7/time_agnostic/ra/2> <http://xmlns.com/foaf/0.1/name> "Springer Science and Business Media LLC"'
                ]
            }
        }
        self.assertEqual(output, expected_output)

    def test_get_state_at_time_no_hooks(self):
        input_1 = "https://github.com/arcangelo7/time_agnostic/ar/1"
        input_2 = "2021-06-05T18:06:55.000Z"
        output = _to_nt_sorted_list(AgnosticEntity(input_1).get_state_at_time(input_2, get_hooks=False))
        expected_output = [
            '<https://github.com/arcangelo7/time_agnostic/ar/1> <http://purl.org/spar/pro/isHeldBy> <https://github.com/arcangelo7/time_agnostic/ra/4>', 
            '<https://github.com/arcangelo7/time_agnostic/ar/1> <http://purl.org/spar/pro/withRole> <http://purl.org/spar/pro/author>', 
            '<https://github.com/arcangelo7/time_agnostic/ar/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/pro/RoleInTime>'
        ]
        self.assertEqual(output, expected_output)

    def test_get_state_at_time_with_hooks(self):
        input_1 = "https://github.com/arcangelo7/time_agnostic/ar/1"
        input_2 = "2021-06-05T18:06:55.000Z"
        output = AgnosticEntity(input_1).get_state_at_time(input_2, get_hooks=True)
        output = (_to_nt_sorted_list(output[0]), output[1])
        expected_output = (
            [
                '<https://github.com/arcangelo7/time_agnostic/ar/1> <http://purl.org/spar/pro/isHeldBy> <https://github.com/arcangelo7/time_agnostic/ra/4>', 
                '<https://github.com/arcangelo7/time_agnostic/ar/1> <http://purl.org/spar/pro/withRole> <http://purl.org/spar/pro/author>', 
                '<https://github.com/arcangelo7/time_agnostic/ar/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/pro/RoleInTime>'
            ],
            {
                'https://github.com/arcangelo7/time_agnostic/ar/1/prov/se/5': '2021-06-05T18:07:00.000Z', 
                'https://github.com/arcangelo7/time_agnostic/ar/1/prov/se/3': '2021-06-05T18:06:41.000Z', 
                'https://github.com/arcangelo7/time_agnostic/ar/1/prov/se/2': '2021-06-05T18:06:34.000Z'
            }
        )
        self.assertEqual(output, expected_output)

    def test__get_entity_current_state(self):
        input = "https://github.com/arcangelo7/time_agnostic/id/1"
        output = _to_dict_of_nt_sorted_lists(AgnosticEntity(input)._get_entity_current_state())
        expected_output = {
            'https://github.com/arcangelo7/time_agnostic/id/1': {
                Literal('2021-06-04T09:36:53+00:00', datatype=URIRef('http://www.w3.org/2001/XMLSchema#dateTime')): None, 
                Literal('2021-06-04T11:15:32+00:00', datatype=URIRef('http://www.w3.org/2001/XMLSchema#dateTime')): [
                    '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-29T16:20:22+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <http://www.w3.org/ns/prov#generatedAtTime> "2021-06-04T09:36:53+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <https://w3id.org/oc/ontology/hasUpdateQuery> "DELETE DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028087\\\\"^^<http://www.w3.org/2001/XMLSchema#string> .} }; INSERT DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028088\\\\" .} }"^^<http://www.w3.org/2001/XMLSchema#string>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/3> <http://www.w3.org/ns/prov#generatedAtTime> "2021-06-04T11:15:32+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/3> <https://w3id.org/oc/ontology/hasUpdateQuery> "DELETE DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028088\\\\"^^<http://www.w3.org/2001/XMLSchema#string> .} }; INSERT DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028089\\\\" .} }"^^<http://www.w3.org/2001/XMLSchema#string>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028089"', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>'], 
                Literal('2021-05-29T16:20:22+00:00', datatype=URIRef('http://www.w3.org/2001/XMLSchema#dateTime')): None
                }
            }
        self.assertEqual(output, expected_output)
    
    def test__old_graphs(self):
        input_1 = "https://github.com/arcangelo7/time_agnostic/id/1"
        input_2 = AgnosticEntity(input_1)._get_entity_current_state()
        output = _to_dict_of_nt_sorted_lists(AgnosticEntity(input_1)._get_old_graphs(input_2))
        expected_output = {
            'https://github.com/arcangelo7/time_agnostic/id/1': {
                datetime.datetime(2021, 6, 4, 11, 15, 32, tzinfo=tzutc()): [
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028089"', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>'], 
                datetime.datetime(2021, 6, 4, 9, 36, 53, tzinfo=tzutc()): [
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028088"^^<http://www.w3.org/2001/XMLSchema#string>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>'], 
                datetime.datetime(2021, 5, 29, 16, 20, 22, tzinfo=tzutc()): [
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028087"^^<http://www.w3.org/2001/XMLSchema#string>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028088"^^<http://www.w3.org/2001/XMLSchema#string>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>'
                ]
            }
        }
        self.assertEqual(output, expected_output)
    
    def test__manage_long_update_queries_insert_data_only(self):
        input_1 = ConjunctiveGraph()
        input_2 = """
            DELETE DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/br/> { 
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/pro/isDocumentContextFor> <https://github.com/arcangelo7/time_agnostic/ar/2995> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15717> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12885> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12855> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12894> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12833> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12875> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12900> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/dc/terms/title> 
                "Citation histories of scientific publications. The data sources"^^<http://www.w3.org/2001/XMLSchema#string> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12892> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12872> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15713> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12859> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12883> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15665> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12853> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15725> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12870> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12886> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12824> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15723> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15660> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15702> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12823> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12864> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12908> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12917> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15748> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15686> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12916> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15680> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15757> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15678> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12844> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15746> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12862> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12921> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15739> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12888> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15659> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15685> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12832> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15704> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15735> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12831> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12882> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12902> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15756> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12877> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12871> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15692> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15699> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12881> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12889> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12825> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12914> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/fabio/Expression> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12912> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12841> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12913> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12838> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15722> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15721> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12865> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15733> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15726> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12849> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15697> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12884> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15698> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12904> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15701> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#partOf> <https://github.com/arcangelo7/time_agnostic/br/15657> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12878> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12876> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15681> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15716> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12856> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15740> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12879> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15658> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15719> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12848> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12822> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15693> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15664> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12899> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12905> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15663> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12897> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12827> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12826> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15661> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15676> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15747> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15755> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15668> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15684> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15696> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15734> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12919> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15683> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12866> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15669> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15728> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12911> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15743> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12898> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15750> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12907> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12893> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15712> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12869> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15674> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#embodiment> <https://github.com/arcangelo7/time_agnostic/re/2015> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12837> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15707> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15662> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15666> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15752> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12920> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15718> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15738> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15753> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12821> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12846> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15689> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12918> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15729> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12903> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12895> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12836> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12851> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15709> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15742> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12861> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12915> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15673> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15679> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15671> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15758> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15751> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15670> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12867> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15691> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12839> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12896> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15675> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12890> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15714> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12842> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://prismstandard.org/namespaces/basic/2.0/publicationDate> 
                "1985-01-01"^^<http://www.w3.org/2001/XMLSchema#gYear> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15754> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15727> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15688> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15737> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15690> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12834> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15677> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12860> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12828> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15672> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15667> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15695> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15705> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15687> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12857> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12887> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15682> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12847> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12854> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15706> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/fabio/JournalArticle> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15715> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/datacite/hasIdentifier> <https://github.com/arcangelo7/time_agnostic/id/13890> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15736> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12863> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15731> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15703> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12910> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12909> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15749> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12840> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15710> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12829> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15711> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15730> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12891> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15744> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12873> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15700> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12852> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12906> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15732> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12858> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15720> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15724> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15708> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12901> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12880> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12843> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12835> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12830> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12874> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15745> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15694> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12845> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12868> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12850> .
            <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15741> .} }
            """
        AgnosticEntity._manage_update_queries(input_1, input_2)
        output = _to_nt_sorted_list(input_1)
        expected_output = [
            '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/dc/terms/title> "Citation histories of scientific publications. The data sources"^^<http://www.w3.org/2001/XMLSchema#string>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15658>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15659>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15660>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15663>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15664>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15665>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15678>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15680>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15681>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15685>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15686>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15692>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15693>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15697>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15698>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15699>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15701>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15702>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15704>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15713>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15716>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15717>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15719>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15721>', 
            '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15722>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15723>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15725>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15726>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15733>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15735>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15739>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15740>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15746>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15748>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15756>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15757>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/pro/isDocumentContextFor> <https://github.com/arcangelo7/time_agnostic/ar/2995>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12822>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12823>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12824>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12825>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12831>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12832>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12833>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12838>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12841>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12844>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12848>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12849>', 
            '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12853>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12855>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12856>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12859>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12862>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12864>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12865>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12870>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12871>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12872>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12875>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12876>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12877>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12878>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12879>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12881>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12882>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12883>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12884>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12885>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12886>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12888>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12889>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12892>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12894>', 
            '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12897>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12899>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12900>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12902>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12904>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12905>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12908>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12912>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12913>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12914>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12916>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12917>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12921>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#partOf> <https://github.com/arcangelo7/time_agnostic/br/15657>', '<https://github.com/arcangelo7/time_agnostic/br/15655> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/fabio/Expression>'
        ]
        self.assertEqual(output, expected_output)

    def test__manage_update_queries_if_short_query(self):
        input_1 = ConjunctiveGraph()
        input_1.add((
            rdflib.term.URIRef('https://github.com/arcangelo7/time_agnostic/id/1'), 
            rdflib.term.URIRef('http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue'), 
            rdflib.term.Literal('10.1007/bf02028088', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#string')), 
            rdflib.term.URIRef("https://github.com/arcangelo7/time_agnostic/id/")
        ))
        input_2 = """
            DELETE DATA { 
                GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { 
                    <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028087"^^<http://www.w3.org/2001/XMLSchema#string> .
                } 
            };
            INSERT DATA { 
                GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { 
                    <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028088"^^<http://www.w3.org/2001/XMLSchema#string> .
                } 
            }
        """
        AgnosticEntity._manage_update_queries(input_1, input_2)
        output = _to_nt_sorted_list(input_1)
        expected_output = ['<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028087"^^<http://www.w3.org/2001/XMLSchema#string>']
        self.assertEqual(output, expected_output)

    def test__query_dataset(self):
        input = AgnosticEntity("https://github.com/arcangelo7/time_agnostic/id/1")
        output = _to_nt_sorted_list(input._query_dataset())
        expected_output = [
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028089"', 
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>'
        ]
        self.assertEqual(output, expected_output)
    
    def test__query_provenance(self):
        input = AgnosticEntity("https://github.com/arcangelo7/time_agnostic/id/1")
        output = _to_nt_sorted_list(input._query_provenance())
        expected_output = [
            '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-29T16:20:22+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <http://www.w3.org/ns/prov#generatedAtTime> "2021-06-04T09:36:53+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <https://w3id.org/oc/ontology/hasUpdateQuery> "DELETE DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028087\\\\"^^<http://www.w3.org/2001/XMLSchema#string> .} }; INSERT DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028088\\\\" .} }"^^<http://www.w3.org/2001/XMLSchema#string>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/3> <http://www.w3.org/ns/prov#generatedAtTime> "2021-06-04T11:15:32+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/3> <https://w3id.org/oc/ontology/hasUpdateQuery> "DELETE DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028088\\\\"^^<http://www.w3.org/2001/XMLSchema#string> .} }; INSERT DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028089\\\\" .} }"^^<http://www.w3.org/2001/XMLSchema#string>'
        ]
        self.assertEqual(output, expected_output)

    def test__convert_to_datetime(self):
        input = "2021-05-21T19:08:56+00:00"
        expected_output = datetime.datetime(2021, 5, 21, 19, 8, 56, tzinfo=datetime.timezone.utc)
        self.assertEqual(AgnosticEntity._convert_to_datetime(input), expected_output)


class Test_support(unittest.TestCase):
    def test_import_json(self):
        input = "./test/config.json"
        expected_output = {
            "dataset": {
                "triplestore_urls": ["http://localhost:9999/blazegraph/sparql"],
                "file_paths": []
            },
            "provenance": {
                "triplestore_urls": [],
                "file_paths": ["./test/scientometrics_prov.json"]
            }
        }
        self.assertEqual(FileManager(input).import_json(), expected_output)


class Test_Sparql(unittest.TestCase):
    def test_run_select_query(self):
        input = """
            SELECT ?p ?o
            WHERE {
                BIND (<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> AS ?s) 
                ?s ?p ?o
            }
        """
        output = Sparql("./test/config.json").run_select_query(input)
        expected_output = {
            ('http://www.w3.org/ns/prov#invalidatedAtTime', '2021-06-04T09:36:53.000Z'), 
            ('http://www.w3.org/ns/prov#specializationOf', 'https://github.com/arcangelo7/time_agnostic/id/1'), 
            ('http://www.w3.org/ns/prov#generatedAtTime', '2021-05-29T16:20:22.000Z'), 
            ('http://www.w3.org/ns/prov#wasAttributedTo', 'https://orcid.org/0000-0002-8420-0696'), 
            ('http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/ns/prov#Entity'), 
            ('http://purl.org/dc/terms/description', "The entity 'https://github.com/arcangelo7/time_agnostic/id/1' has been created.")
        }
        self.assertEqual(output, expected_output)
    
    def test__get_tuples_from_file(self):
        input_1 = """
            SELECT ?p ?o
            WHERE {
                BIND (<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> AS ?s) 
                ?s ?p ?o
            }
        """
        input_2 = {
            "triplestore_urls": [],
            "file_paths": ["./test/scientometrics_prov.json"]
        }
        output = Sparql._get_tuples_from_files(input_1, input_2)
        expected_output = {
            ('http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/ns/prov#Entity'), 
            ('http://purl.org/dc/terms/description', "The entity 'https://github.com/arcangelo7/time_agnostic/id/1' has been created."), 
            ('http://www.w3.org/ns/prov#wasAttributedTo', 'https://orcid.org/0000-0002-8420-0696'), 
            ('http://www.w3.org/ns/prov#specializationOf', 'https://github.com/arcangelo7/time_agnostic/id/1'), 
            ('http://www.w3.org/ns/prov#generatedAtTime', '2021-05-06T18:14:42')
        }
        self.assertEqual(output, expected_output)
    
    def test__get_tuples_from_triplestores(self):
        input_1 = """
            SELECT ?p ?o
            WHERE {
                BIND (<https://github.com/arcangelo7/time_agnostic/id/1> AS ?s)
                ?s ?p ?o
            }
        """
        input_2 = {
            "triplestore_urls": ["http://localhost:9999/blazegraph/sparql"],
            "file_paths": []
        }
        output = Sparql._get_tuples_from_triplestores(input_1, input_2)
        expected_output = {
            ('http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue', '10.1007/bf02028089'), 
            ('http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://purl.org/spar/datacite/Identifier'), 
            ('http://purl.org/spar/datacite/usesIdentifierScheme', 'http://purl.org/spar/datacite/doi')
        }
        self.assertEqual(output, expected_output)
    
    def test_run_construct_query(self):
        input = """
            SELECT ?s ?p ?o ?c
            WHERE {
                GRAPH ?c {?s ?p ?o}
                BIND (<https://github.com/arcangelo7/time_agnostic/id/1> as ?s)
            }           
        """
        output = _to_nt_sorted_list(Sparql("./test/config.json").run_construct_query(input))
        expected_output = [
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028089"', 
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>'
        ]
        self.assertEqual(output, expected_output)
    
    def test__get_graph_from_files(self):
        input_1= f"""
            CONSTRUCT {{
                ?snapshot <{ProvEntity.iri_generated_at_time}> ?t;      
                        <{ProvEntity.iri_has_update_query}> ?updateQuery.
            }} 
            WHERE {{
                ?snapshot <{ProvEntity.iri_specialization_of}> <https://github.com/arcangelo7/time_agnostic/id/1>;
                        <{ProvEntity.iri_generated_at_time}> ?t.
            OPTIONAL {{
                    ?snapshot <{ProvEntity.iri_has_update_query}> ?updateQuery.
                }}   
            }}
        """       
        input_2 = {
            "triplestore_urls": [],
            "file_paths": ["./test/scientometrics_prov.json"]
        }
        output = _to_nt_sorted_list(Sparql("./test/config.json")._get_graph_from_files(input_1, input_2)) 
        expected_output = ['<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-06T18:14:42"^^<http://www.w3.org/2001/XMLSchema#dateTime>']
        self.assertEqual(output, expected_output)
    
    def test__get_graph_from_triplestores(self):
        input_1= f"""
            CONSTRUCT {{
                ?snapshot <{ProvEntity.iri_generated_at_time}> ?t;      
                        <{ProvEntity.iri_has_update_query}> ?updateQuery.
            }} 
            WHERE {{
                ?snapshot <{ProvEntity.iri_specialization_of}> <https://github.com/arcangelo7/time_agnostic/id/1>;
                        <{ProvEntity.iri_generated_at_time}> ?t.
            OPTIONAL {{
                    ?snapshot <{ProvEntity.iri_has_update_query}> ?updateQuery.
                }}   
            }}
        """       
        input_2 = {
            "triplestore_urls": ["http://localhost:9999/blazegraph/sparql"],
            "file_paths": []
        }
        output = _to_nt_sorted_list(Sparql("./test/config.json")._get_graph_from_triplestores(input_1, input_2)) 
        expected_output = [
            '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-29T16:20:22+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <http://www.w3.org/ns/prov#generatedAtTime> "2021-06-04T09:36:53+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <https://w3id.org/oc/ontology/hasUpdateQuery> "DELETE DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028087\\\\"^^<http://www.w3.org/2001/XMLSchema#string> .} }; INSERT DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028088\\\\" .} }"^^<http://www.w3.org/2001/XMLSchema#string>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/3> <http://www.w3.org/ns/prov#generatedAtTime> "2021-06-04T11:15:32+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/3> <https://w3id.org/oc/ontology/hasUpdateQuery> "DELETE DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028088\\\\"^^<http://www.w3.org/2001/XMLSchema#string> .} }; INSERT DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028089\\\\" .} }"^^<http://www.w3.org/2001/XMLSchema#string>'
        ]
        self.assertEqual(output, expected_output)


    def test__cut_by_limit(self):
        input_1 = """
            SELECT ?p ?o
            WHERE {
                BIND (<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> AS ?s)
                ?s ?p ?o
            }
            LIMIT 2
        """
        input_2 = [
            ('http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/ns/prov#Entity'), 
            ('http://purl.org/dc/terms/description', "The entity 'https://github.com/arcangelo7/time_agnostic/id/1' has been created."), 
            ('http://www.w3.org/ns/prov#wasAttributedTo', 'https://orcid.org/0000-0002-8420-0696'), 
            ('http://www.w3.org/ns/prov#specializationOf', 'https://github.com/arcangelo7/time_agnostic/id/1'), 
            ('http://www.w3.org/ns/prov#generatedAtTime', '2021-05-06T18:14:42')
        ]
        output = len(Sparql._cut_by_limit(input_1, input_2))
        expected_output = 2
        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
