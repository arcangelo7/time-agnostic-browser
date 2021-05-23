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
from typing import Union, Set, Tuple

import re, itertools
from SPARQLWrapper import SPARQLWrapper, XML, POST, RDFXML, JSON
from rdflib import Graph
from oc_ocdm import Reader
from rdflib.term import URIRef
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
    
    def execute_query(self, query:str) -> Union[Set[Tuple[URIRef, URIRef]], Graph]:
        if "select" in query.lower():
            output = set()
            format = JSON
            if len(self.endpoints) > 0:
                output.update(self._query_endpoints(query, format=format))
            if len(self.file_paths) > 0:
                output.update(self._query_files(query, format=format))
        elif "construct" in query.lower():
            output = Graph()
            format = RDFXML
            if len(self.endpoints) > 0:
                output += self._query_endpoints(query, format=format)
            if len(self.file_paths) > 0:
                output += self._query_files(query, format=format)
        if "limit" in query.lower():
            limit = int(re.search("(?:limit\s*)(\d+)", query, re.IGNORECASE).group(1))
            if format == JSON:
                output = set(itertools.islice(output, limit))
            elif format == RDFXML:
                new_output = Graph()
                for triple in list(output.triples((None, None, None)))[:limit]:
                    new_output.add(triple)
                output = new_output
        return output
    
    def _query_endpoints(self, 
            query:str, 
            format:Union[RDFXML, JSON]) -> Union[Set[Tuple[URIRef, URIRef]], Graph]:
        if format == RDFXML:
            output = Graph()
        elif format == JSON:
            output = set()
        for endpoint in self.endpoints:
            sparql = SPARQLWrapper(endpoint=endpoint)
            sparql.setQuery(query)
            # POST is required to avoid the query length limit imposed by the GET method
            sparql.setMethod(POST)
            sparql.setReturnFormat(format)
            results = sparql.queryAndConvert()
            if format == JSON:
                for result_dict in results["results"]["bindings"]:
                    output.add(tuple(d["value"] for d in result_dict.values()))
            elif format == RDFXML:
                output += results
        return output
    
    def _query_files(self, 
            query:str, 
            format:Union[RDFXML, JSON]) -> Union[Set[Tuple[URIRef, URIRef]], Graph]:
        g = Graph()
        if format == RDFXML:
            output = Graph()
        elif format == JSON:
            output = set()
        for file_path in self.file_paths:
            g += Reader().load(file_path)
        results = g.query(query)
        if format == RDFXML:
            output += results
        elif format == JSON:
            for tuple in results:
                output.add(tuple)
        return output

query = "SELECT ?s ?p ?o WHERE {?s ?p ?o; a <http://www.w3.org/ns/prov#Entity>} LIMIT 10"
output = Sparql().execute_query(query=query)
print(len(output))
print(output)
