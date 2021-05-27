from sparql import Sparql
from SPARQLWrapper import XML, SPARQLWrapper, JSON, POST
from rdflib import URIRef, Literal, Graph, ConjunctiveGraph
from rdflib.plugins.sparql.processor import processUpdate
from rdflib.plugins.sparql.sparql import QueryContext
from pprint import pprint
from agnostic_query import Agnostic_query

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

entities_histories = Agnostic_query.get_entities_histories({"https://github.com/arcangelo7/time_agnostic/br/1", "https://github.com/arcangelo7/time_agnostic/id/1"}, True)
pprint(entities_histories)








