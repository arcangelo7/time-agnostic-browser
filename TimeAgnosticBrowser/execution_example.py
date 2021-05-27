from sparql import Sparql
from SPARQLWrapper import XML, SPARQLWrapper, JSON, POST
from rdflib import URIRef, Literal, Graph, ConjunctiveGraph
from rdflib.plugins.sparql.processor import processUpdate
from rdflib.plugins.sparql.sparql import QueryContext
from pprint import pprint
from agnostic_query import Agnostic_query
from agnostic_entity import Agnostic_entity, get_entities_histories

# query = """
# SELECT ?s ?p ?o
# WHERE {
#     VALUES ?s {<https://github.com/arcangelo7/time_agnostic/id/1>}
#     ?s ?p ?o.
# }
# """
# agnostic_query = Agnostic_query(query)
# result = agnostic_query.run_agnostic_query("https://github.com/arcangelo7/time_agnostic/")
# print(result)

agnostic_entity = Agnostic_entity("https://github.com/arcangelo7/time_agnostic/id/1", related_entities_history=True)

entity_state = agnostic_entity.get_state_at_time("2021-05-21T19:08:56+00:00")
pprint(entity_state)









