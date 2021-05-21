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

from typing import Union
import json
from SPARQLWrapper import SPARQLWrapper, JSON, XML, POST
from rdflib import Graph

CONFIG_PATH = "./config.json"

class File_manager:
    @staticmethod
    def import_json(path:str) -> dict:
        with open(path, encoding="utf8") as json_file:
            return json.load(json_file)

class Sparql:
    def __init__(self, config_path:str=CONFIG_PATH):
        self.config_path = config_path
        self.endpoints:list = File_manager.import_json(path=self.config_path)["triplestore_url"]
        self.file_paths:list = File_manager.import_json(path=self.config_path)["file_path"]
    
    def _execute_query(self, query:str, format:Union[JSON, XML]) -> Union[JSON, XML, Graph]:
        output = dict()
        if len(self.endpoints)>0:
            for endpoint in self.endpoints:
                sparql = SPARQLWrapper(endpoint=endpoint, returnFormat=format)
                sparql.setQuery(query)
                sparql.setReturnFormat(format)
                # POST is required to avoid the query length limit imposed by the GET method
                sparql.setMethod(POST)
                results = sparql.query().convert()
                if format == JSON:
                    if output:
                        output["results"]["bindings"].extend(results["results"]["bindings"])
                    else:
                        output = results
                else:
                    return results
        return Sparql._merge_identical_outputs(output)
    
    @classmethod
    def _merge_identical_outputs(cls, output:dict) -> dict:
        merged_output = list()
        for result in output["results"]["bindings"]:
            if result not in merged_output:
                merged_output.append(result)
        output["results"]["bindings"] = merged_output
        return output





