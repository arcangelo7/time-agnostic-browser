import agnostic_query
from sparql import Sparql
from SPARQLWrapper import XML, SPARQLWrapper, JSON, POST
from rdflib import URIRef, Literal, Graph, ConjunctiveGraph
from rdflib.plugins.sparql.processor import processUpdate
from rdflib.plugins.sparql.sparql import QueryContext
from pprint import pprint
from agnostic_query import Agnostic_query

agnostic_query = Agnostic_query()

entity_current_state = agnostic_query._get_entity_current_state("https://github.com/arcangelo7/time_agnostic/id/1")
old_graphs = agnostic_query._get_old_graphs(entity_current_state, "https://github.com/arcangelo7/time_agnostic/id/1")
update_query = 'INSERT DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028087"^^<http://www.w3.org/2001/XMLSchema#string> .} }; DELETE DATA { GRAPH <https://github.com/arcangelo7/time_agnostic/id/> { <https://github.com/arcangelo7/time_agnostic/id/1> <http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue> "10.1007/bf02028088" .} }'
for k,v in old_graphs.items():
    for k,v in v.items():
        for quad in v.quads():
            pprint(quad)
        print("\n")









