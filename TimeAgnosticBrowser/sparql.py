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

import re, itertools, rdflib
from SPARQLWrapper import SPARQLWrapper, POST, RDFXML, JSON, N3, XML
from rdflib import Graph, ConjunctiveGraph
from oc_ocdm import Reader
from rdflib.term import URIRef, Literal
from support import File_manager
from prov_entity import ProvEntity
from rdflib.plugins.sparql.processor import prepareQuery
from rdflib.plugins.sparql.sparql import Query
from rdflib.plugins.sparql.sparql import Prologue
from rdflib.plugins.sparql.parserutils import CompValue

CONFIG_PATH = "./config.json"

class Sparql:
    def __init__(self, config_path:str=CONFIG_PATH):
        """
        The Sparql class is instantiated by passing as a parameter 
        the path of a configuration file, whose default location is "./config.json"
        """
        self.config_path = config_path
        self.config:list = File_manager.import_json(path=self.config_path)
    
    def _run_the_query(self, query:str):
        cg = ConjunctiveGraph()
        if ProvEntity.PROV in query:
            storer:dict = self.config["provenance"]
        else:
            storer:dict = self.config["dataset"]
        if len(storer["file_paths"]) > 0:
            results = self._query_files(query, storer)
            for quad in results.quads():
                cg.add(quad)
        if len(storer["triplestore_urls"]) > 0:
            results = self._query_triplestores(query, storer)
            for quad in results.quads():
                cg.add(quad)
        return cg
    
    @classmethod
    def _query_files(cls, query:str, storer:dict) -> ConjunctiveGraph:
        cg = ConjunctiveGraph()
        storer = storer["file_paths"]
        for file_path in storer:
            file_cg = ConjunctiveGraph()
            file_cg.parse(location=file_path, format="json-ld")
            results = file_cg.query(query)
            for result in results:
                cg.add(result)
        return cg

    @classmethod
    def _query_triplestores(cls, query:str, storer:dict) -> ConjunctiveGraph:
        cg = ConjunctiveGraph()
        storer = storer["triplestore_urls"]
        prepare_query:Query = prepareQuery(query)
        algebra:CompValue = prepare_query.algebra
        for url in storer:
            sparql = SPARQLWrapper(url)
            sparql.setMethod(POST)
            sparql.setQuery(query)
            if algebra.name == "SelectQuery":
                sparql.setReturnFormat(JSON)
                results = sparql.queryAndConvert()
                for quad in results["results"]["bindings"]:
                    quad_to_add = list()
                    for var in results["head"]["vars"]:
                        if quad[var]["type"] == "uri":
                            quad_to_add.append(URIRef(quad[var]["value"]))
                        elif quad[var]["type"] == "literal":
                            quad_to_add.append(Literal(quad[var]["value"]))
                    cg.add(tuple(quad_to_add))
            elif algebra.name == "ConstructQuery":
                sparql.setReturnFormat(RDFXML)
                cg += sparql.queryAndConvert()            
        return cg
        


    

