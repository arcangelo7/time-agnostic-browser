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

from SPARQLWrapper import SPARQLWrapper, XML, POST
from rdflib import Graph
from oc_ocdm import Reader
from support import File_manager

CONFIG_PATH = "./config.json"

class Sparql:
    def __init__(self, config_path:str=CONFIG_PATH):
        """
        The Sparql class is instantiated by passing as a parameter 
        the path of a configuration file, whose default location is "./config.json"
        """
        self.config_path = config_path
        self.endpoints:list = File_manager.import_json(path=self.config_path)["triplestore_url"]
        self.file_paths:list = File_manager.import_json(path=self.config_path)["file_path"]
    
    def execute_query(self, query:str) -> Graph:
        output = Graph()
        if len(self.endpoints) > 0:
            output += self._query_endpoints(query)
        if len(self.file_paths) > 0:
            output += self._query_files(query)
        return output

    def _query_endpoints(self, query:str) -> Graph:
        output = Graph()
        for endpoint in self.endpoints:
            sparql = SPARQLWrapper(endpoint=endpoint)
            sparql.setQuery(query)
            sparql.setReturnFormat(XML)
            # POST is required to avoid the query length limit imposed by the GET method
            sparql.setMethod(POST)
            results = sparql.query().convert()
            # print(results)
            # g = Graph()
            # g.parse(data=results.toxml(), format="xml")
            # output += g
        return output
    
    def _query_files(self, query:str):
        g = Graph()
        for file_path in self.file_paths:
            g += Reader().load(file_path)
        results = g.query(query)
        output = Graph()
        for result in results:
            output.add(result)
        return output

query = "SELECT ?s ?p ?o WHERE {?s ?p ?o; a <http://www.w3.org/ns/prov#Entity>} LIMIT 10"
output = Sparql().execute_query(query=query)
# for triple in output.triples((None, None, None)):
#     print(triple)