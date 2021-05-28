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

from typing import Dict

import json, os, zipfile
from zipfile import ZipFile
from rdflib.graph import ConjunctiveGraph


class File_manager:
    def __init__(self, path:str):
        self.path = path
        
    def import_json(self) -> dict:
        with open(self.path, encoding="utf8") as json_file:
            return json.load(json_file)

    def _zipdir(self, ziph:ZipFile) -> None:
        for root, dirs, files in os.walk(self.path):
            dirs[:] = [d for d in dirs if d != "small"]
            for file in files:
                ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(self.path, '..')))
    
    def zip_data(self) -> None:
        zipf = zipfile.ZipFile('output.zip', 'w', zipfile.ZIP_DEFLATED)
        self._zipdir(self.path, zipf)
        zipf.close()

    def minify_json(self) -> None:
        print(f"[Support: INFO] Minifing file {self.path}")
        file_data = open(self.path, "r", encoding="utf-8").read()
        json_data = json.loads(file_data) 
        json_string = json.dumps(json_data, separators=(',', ":")) 
        path = str(self.path).replace(".json", "")
        new_path = "{0}_minify.json".format(path)
        open(new_path, "w+", encoding="utf-8").write(json_string) 

def _to_nt_sorted_list(cg:ConjunctiveGraph) -> list:
    if cg is None:
        return None
    nt_list = str(cg.serialize(format="nt")).split(".\\n")
    sorted_nt_list = sorted([triple.replace("b\'", "").strip() for triple in nt_list if triple != "\\n'"])
    return sorted_nt_list

def _to_dict_of_nt_sorted_lists(dictionary:Dict[str, Dict[str, ConjunctiveGraph]]) -> dict:
    for key, value in dictionary.items():
        if isinstance(value, ConjunctiveGraph):
            dictionary[key] = _to_nt_sorted_list(value)
        else:
            for snapshot, cg in value.items():
                value[snapshot] = _to_nt_sorted_list(cg)
    return dictionary












