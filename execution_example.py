from SPARQLWrapper import XML, SPARQLWrapper, JSON, POST
from SPARQLWrapper.Wrapper import RDFXML
from rdflib import URIRef, Literal, Graph, ConjunctiveGraph
from rdflib.plugins.sparql import sparql
from rdflib.plugins.sparql.processor import processUpdate
from rdflib.plugins.sparql.sparql import QueryContext
from pprint import pprint
import sys

from time_agnostic_browser.sparql import Sparql
from time_agnostic_browser.agnostic_query import Agnostic_query
from time_agnostic_browser.agnostic_entity import AgnosticEntity, get_entities_histories

cg = ConjunctiveGraph()
update_query = """
INSERT DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/br/> { <https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/pro/isDocumentContextFor> <https://github.com/arcangelo7/time_agnostic/ar/2995> .
<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/spar/cito/cites> <https://github.com/arcangelo7/time_agnostic/br/15717> .
<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12885> .
<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12855> .
<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12894> .
<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12833> .
<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12875> .
<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/vocab/frbr/core#part> <https://github.com/arcangelo7/time_agnostic/be/12900> .
<https://github.com/arcangelo7/time_agnostic/br/15655> <http://purl.org/dc/terms/title> "Citation histories of scientific publications. The data sources"^^<http://www.w3.org/2001/XMLSchema#string> .
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
<https://github.com/arcangelo7/time_agnostic/br/15655> <http://prismstandard.org/namespaces/basic/2.0/publicationDate> "1985-01-01"^^<http://www.w3.org/2001/XMLSchema#gYear> .
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
# sys.setrecursionlimit(1900)
processUpdate(cg, update_query)
print("hello")
print(list(cg.quads()))









