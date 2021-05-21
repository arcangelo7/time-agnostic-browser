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

import unittest
from agnostic_query import Agnostic_query
from support import File_manager, Sparql

class Test_Agnostic_query(unittest.TestCase):
    pass

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
    def test_merge_identical_outputs(self):
        input = {'head': {'vars': ['literalValue']}, 'results': {'bindings': [
            {'literalValue': {'type': 'literal', 'value': '10.1007/bf02028087'}}, 
            {'literalValue': {'type': 'literal', 'value': '10.1007/bf02028087'}}
            ]}}
        expected_output = {'head': {'vars': ['literalValue']}, 'results': {'bindings': [
            {'literalValue': {'type': 'literal', 'value': '10.1007/bf02028087'}} 
            ]}}
        self.assertEqual(Sparql._merge_identical_outputs(input), expected_output)

if __name__ == '__main__':
    unittest.main()
