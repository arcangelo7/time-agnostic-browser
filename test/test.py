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

import unittest, rdflib, datetime

from rdflib.graph import ConjunctiveGraph
from agnostic_query import Agnostic_query
from agnostic_entity import Agnostic_entity
from rdflib import Graph, Literal, URIRef
from support import File_manager, _to_nt_sorted_list, _to_dict_of_nt_sorted_lists
from sparql import Sparql
from SPARQLWrapper import JSON, XML
from pprint import pprint
from prov_entity import ProvEntity

class Test_Agnostic_entity(unittest.TestCase):
    def test_get_history(self):
        input = "https://github.com/arcangelo7/time_agnostic/id/1"
        output = _to_dict_of_nt_sorted_lists(Agnostic_entity(input).get_history())
        expected_output = {'https://github.com/arcangelo7/time_agnostic/id/1': 
        {'2021-05-21T19:08:56+00:00': 
            ['<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-14T17:07:03+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-21T19:08:56+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <https://w3id.org/oc/ontology/hasUpdateQuery> "DELETE DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028087\\\\"^^<http://www.w3.org/2001/XMLSchema#string> .} }; INSERT DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028088\\\\" .} }"^^<http://www.w3.org/2001/XMLSchema#string>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028088"', 
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>'], 
        '2021-05-14T17:07:03+00:00': 
            ['<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-14T17:07:03+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028087"^^<http://www.w3.org/2001/XMLSchema#string>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>']}}
        self.assertEqual(output, expected_output)
    
    def test_get_history_and_related_entities(self):
        input = "https://github.com/arcangelo7/time_agnostic/id/1"
        output = _to_dict_of_nt_sorted_lists(Agnostic_entity(input, related_entities_history=True).get_history())
        expected_output = {
            'https://github.com/arcangelo7/time_agnostic/id/1': 
                {'2021-05-21T19:08:56+00:00': [
                    '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-14T17:07:03+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-21T19:08:56+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <https://w3id.org/oc/ontology/hasUpdateQuery> "DELETE DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028087\\\\"^^<http://www.w3.org/2001/XMLSchema#string> .} }; INSERT DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028088\\\\" .} }"^^<http://www.w3.org/2001/XMLSchema#string>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028088"', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>'], 
                '2021-05-14T17:07:03+00:00': [
                    '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-14T17:07:03+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028087"^^<http://www.w3.org/2001/XMLSchema#string>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>']}, 
            'https://github.com/arcangelo7/time_agnostic/br/1': {
                '2021-05-14T17:07:03+00:00': [
                    '<https://github.com/arcangelo7/time_agnostic/br/1/prov/se/1> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-14T17:07:03+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://prismstandard.org/namespaces/basic/2.0/publicationDate> "1992"', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/dc/terms/title> "A validation study of \\\\u201CLEXIMAPPE\\\\u201D"', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/10>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/11>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/12>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/13>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/14>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/16>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/17>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/18>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/19>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/20>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/4>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/5>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/6>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/7>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/8>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/9>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/datacite/hasIdentifier> <https://github.com/arcangelo7/time_agnostic/id/1>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/spar/pro/isDocumentContextFor> <https://github.com/arcangelo7/time_agnostic/ar/1>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#embodiment> <https://github.com/arcangelo7/time_agnostic/re/1>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/10>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/11>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/13>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/14>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/15>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/16>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/17>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/1>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/2>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/3>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/4>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/5>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/6>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/7>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/8>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/9>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://purl.org/vocab/frbr/core#partOf> <https://github.com/arcangelo7/time_agnostic/br/3>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/fabio/Expression>', 
                    '<https://github.com/arcangelo7/time_agnostic/br/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/fabio/JournalArticle>']}}
        self.assertEqual(output, expected_output)

    def test_get_state_at_time(self):
        input_1 = "https://github.com/arcangelo7/time_agnostic/id/1"
        input_2 = "2021-05-21T19:08:56+00:00"
        output = _to_dict_of_nt_sorted_lists(Agnostic_entity(input_1).get_state_at_time(input_2))
        expected_output = {
            '2021-05-21T19:08:56+00:00': 
                ['<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-14T17:07:03+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
                '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-21T19:08:56+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
                '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <https://w3id.org/oc/ontology/hasUpdateQuery> "DELETE DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028087\\\\"^^<http://www.w3.org/2001/XMLSchema#string> .} }; INSERT DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028088\\\\" .} }"^^<http://www.w3.org/2001/XMLSchema#string>', 
                '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
                '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028088"', 
                '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>'], 
            'before': {
                '2021-05-14T17:07:03+00:00': 
                    ['<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-14T17:07:03+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028087"^^<http://www.w3.org/2001/XMLSchema#string>', 
                    '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>']}, 
            'after': {}}
        self.assertEqual(output, expected_output)

    def test__get_entity_current_state(self):
        input = "https://github.com/arcangelo7/time_agnostic/id/1"
        output = _to_dict_of_nt_sorted_lists(Agnostic_entity(input)._get_entity_current_state())
        expected_output = {'https://github.com/arcangelo7/time_agnostic/id/1': {
            Literal('2021-05-14T17:07:03+00:00', datatype=URIRef('http://www.w3.org/2001/XMLSchema#dateTime')): None, 
            Literal('2021-05-21T19:08:56+00:00', datatype=URIRef('http://www.w3.org/2001/XMLSchema#dateTime')): 
                ['<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-14T17:07:03+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
                '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-21T19:08:56+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>',
                '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <https://w3id.org/oc/ontology/hasUpdateQuery> "DELETE DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028087\\\\"^^<http://www.w3.org/2001/XMLSchema#string> .} }; INSERT DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028088\\\\" .} }"^^<http://www.w3.org/2001/XMLSchema#string>', 
                '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
                '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028088"', 
                '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>']}}
        self.assertEqual(output, expected_output)
    
    def test__old_graphs(self):
        input_1 = "https://github.com/arcangelo7/time_agnostic/id/1"
        input_2 = Agnostic_entity(input_1)._get_entity_current_state()
        output = _to_dict_of_nt_sorted_lists(Agnostic_entity(input_1)._get_old_graphs(input_2))
        expected_output = {'https://github.com/arcangelo7/time_agnostic/id/1': 
        {'2021-05-21T19:08:56+00:00': 
            ['<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-14T17:07:03+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-21T19:08:56+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <https://w3id.org/oc/ontology/hasUpdateQuery> "DELETE DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028087\\\\"^^<http://www.w3.org/2001/XMLSchema#string> .} }; INSERT DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028088\\\\" .} }"^^<http://www.w3.org/2001/XMLSchema#string>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028088"', 
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>'], 
        '2021-05-14T17:07:03+00:00': 
            ['<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-14T17:07:03+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028087"^^<http://www.w3.org/2001/XMLSchema#string>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>']}}
        self.assertEqual(output, expected_output)
    
    def test__query_dataset(self):
        input = Agnostic_entity("https://github.com/arcangelo7/time_agnostic/id/1")
        output = _to_nt_sorted_list(input._query_dataset())
        expected_output = ['<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
                           '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028088"', 
                           '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/spar/datacite/Identifier>']
        self.assertEqual(output, expected_output)
    
    def test__query_provenance(self):
        input = Agnostic_entity("https://github.com/arcangelo7/time_agnostic/id/1")
        output = _to_nt_sorted_list(input._query_provenance())
        expected_output = ['<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-14T17:07:03+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
                           '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-21T19:08:56+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>',
                           '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <https://w3id.org/oc/ontology/hasUpdateQuery> "DELETE DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028087\\\\"^^<http://www.w3.org/2001/XMLSchema#string> .} }; INSERT DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028088\\\\" .} }"^^<http://www.w3.org/2001/XMLSchema#string>']
        self.assertEqual(output, expected_output)

    def test__convert_to_datetime(self):
        input = "2021-05-21T19:08:56+00:00"
        expected_output = datetime.datetime(2021, 5, 21, 19, 8, 56, tzinfo=datetime.timezone.utc)
        self.assertEqual(Agnostic_entity._convert_to_datetime(input), expected_output)


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
        self.assertEqual(File_manager(input).import_json(), expected_output)


class Test_Sparql(unittest.TestCase):
    def test_run_select_query(self):
        input = """
            SELECT ?p ?o
            WHERE {
                VALUES ?s {<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1>}
                ?s ?p ?o
            }
        """
        output = Sparql("./test/config.json").run_select_query(input)
        expected_output = {
            ('http://purl.org/dc/terms/description', "The entity 'https://github.com/arcangelo7/time_agnostic/id/1' has been created."), 
            ('http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/ns/prov#Entity'), 
            ('http://www.w3.org/ns/prov#wasAttributedTo', 'https://orcid.org/0000-0002-8420-0696'), 
            ('http://www.w3.org/ns/prov#invalidatedAtTime', '2021-05-21T19:08:56.000Z'), 
            ('http://www.w3.org/ns/prov#generatedAtTime', '2021-05-14T17:07:03.000Z'), 
            ('http://www.w3.org/ns/prov#specializationOf', 'https://github.com/arcangelo7/time_agnostic/id/1')
        }
        self.assertEqual(output, expected_output)
    
    def test__get_tuples_from_file(self):
        input_1 = """
            SELECT ?p ?o
            WHERE {
                VALUES ?s {<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1>}
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
                VALUES ?s {<https://github.com/arcangelo7/time_agnostic/id/1>}
                ?s ?p ?o
            }
        """
        input_2 = {
            "triplestore_urls": ["http://localhost:9999/blazegraph/sparql"],
            "file_paths": []
        }
        output = Sparql._get_tuples_from_triplestores(input_1, input_2)
        expected_output = {
            ('http://purl.org/spar/datacite/usesIdentifierScheme', 'http://purl.org/spar/datacite/doi'), 
            ('http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://purl.org/spar/datacite/Identifier'), 
            ('http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue', '10.1007/bf02028088')
        }
        self.assertEqual(output, expected_output)
    
    def test_run_construct_query(self):
        input = """
            SELECT ?s ?p ?o ?c
            WHERE {
                GRAPH ?c {?s ?p ?o}
                VALUES ?s {<https://github.com/arcangelo7/time_agnostic/id/1>}
            }           
        """
        output = _to_nt_sorted_list(Sparql("./test/config.json").run_construct_query(input))
        expected_output = [
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://purl.org/spar/datacite/usesIdentifierScheme> <http://purl.org/spar/datacite/doi>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028088"', 
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
            '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-14T17:07:03+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <http://www.w3.org/ns/prov#generatedAtTime> "2021-05-21T19:08:56+00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', 
            '<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/2> <https://w3id.org/oc/ontology/hasUpdateQuery> "DELETE DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028087\\\\"^^<http://www.w3.org/2001/XMLSchema#string> .} }; INSERT DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> \\\\"10.1007/bf02028088\\\\" .} }"^^<http://www.w3.org/2001/XMLSchema#string>']
        self.assertEqual(output, expected_output)


    def test__cut_by_limit(self):
        input_1 = """
            SELECT ?p ?o
            WHERE {
                VALUES ?s {<https://github.com/arcangelo7/time_agnostic/id/1/prov/se/1>}
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
