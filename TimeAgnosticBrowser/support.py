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
import json, os, zipfile
from SPARQLWrapper import SPARQLWrapper, XML, POST
from SPARQLWrapper.Wrapper import RDFXML, N3
from rdflib import Graph
from zipfile import ZipFile
from oc_ocdm import Reader


class File_manager:
    @classmethod
    def import_json(cls, path:str) -> dict:
        with open(path, encoding="utf8") as json_file:
            return json.load(json_file)

    @classmethod
    def _zipdir(cls, path:str, ziph:ZipFile) -> None:
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d != "small"]
            for file in files:
                ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))
    
    @classmethod
    def zip_data(cls, path:str) -> None:
        zipf = zipfile.ZipFile('output.zip', 'w', zipfile.ZIP_DEFLATED)
        cls._zipdir(path, zipf)
        zipf.close()

    @classmethod
    def minify_json(cls, path:str) -> None:
        print(f"[Support: INFO] Minifing file {path}")
        file_data = open(path, "r", encoding="utf-8").read()
        json_data = json.loads(file_data) 
        json_string = json.dumps(json_data, separators=(',', ":")) 
        path = str(path).replace(".json", "")
        new_path = "{0}_minify.json".format(path)
        open(new_path, "w+", encoding="utf-8").write(json_string) 











