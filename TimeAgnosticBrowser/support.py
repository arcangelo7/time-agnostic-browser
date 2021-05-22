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

from logging import raiseExceptions
from typing import Union
import json
from warnings import formatwarning
from SPARQLWrapper import SPARQLWrapper, JSON, XML, POST
from rdflib import Graph

CONFIG_PATH = "./config.json"

class File_manager:
    @classmethod
    def import_json(cls, path:str) -> dict:
        with open(path, encoding="utf8") as json_file:
            return json.load(json_file)

class Sparql:
    def __init__(self, config_path:str=CONFIG_PATH):
        """
        The Sparql class is instantiated by passing as a parameter 
        the path of a configuration file, whose default location is "./config.json"
        """
        self.config_path = config_path
        self.endpoints:list = File_manager.import_json(path=self.config_path)["triplestore_url"]
        self.file_paths:list = File_manager.import_json(path=self.config_path)["file_path"]
    
    def execute_query(self, query:str, format:Union[JSON, XML]) -> Union[JSON, XML, Graph]:
        if len(self.endpoints) > 0:
            output = self._query_endpoints(query, format)
        if len(self.file_paths) > 0:
            output = self._query_files(query, format)
        return self._merge_identical_outputs(output, format)

    def _manage_json_output(self, results:dict, output:dict):
        if output:
            output["results"]["bindings"].extend(results["results"]["bindings"])
        else:
            output = results
        return output

    def _manage_xml_output(self, results:Graph, output:Graph):
        for triple in results.triples((None, None, None)):
            output.add(triple)
        return output

    def _query_endpoints(self, query:str, format:Union[JSON, XML]) -> Union[JSON, XML, Graph]:
        if format == JSON:
            output = dict()
        elif format == XML:
            output = Graph()
        else:
            raise(ValueError("Please, choose a valid format. You can currently choose between XML or JSON"))
        for endpoint in self.endpoints:
            sparql = SPARQLWrapper(endpoint=endpoint, returnFormat=format)
            sparql.setQuery(query)
            sparql.setReturnFormat(format)
            # POST is required to avoid the query length limit imposed by the GET method
            sparql.setMethod(POST)
            results = sparql.query().convert()
            if format == JSON:
                output = self._manage_json_output(results, output)
            elif format == XML:
                output = self._manage_xml_output(results, output)                
        return output
    
    def _query_files(self, query:str, format:Union[JSON, XML]):
        if format == JSON:
            output = dict()
        elif format == XML:
            output:Graph = Graph()
        else:
            raise(ValueError("Please, choose a valid format. You can currently choose between XML or JSON"))
        for file_path in self.file_paths:
            output.parse(location=file_path, format="json-ld")
            output.query(query)
        return output
            
    def _merge_identical_outputs(self, output:Union[dict, Graph], format:Union[JSON, XML]) -> dict:
        if format == JSON:
            merged_output = list()
            for result in output["results"]["bindings"]:
                if result not in merged_output:
                    merged_output.append(result)
            output["results"]["bindings"] = merged_output
        return output











