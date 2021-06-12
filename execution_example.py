from datetime import time
from SPARQLWrapper import XML, SPARQLWrapper, JSON, POST
from SPARQLWrapper.Wrapper import RDFXML
from rdflib import URIRef, Literal, Graph, ConjunctiveGraph
from rdflib.plugins.sparql import sparql
from rdflib.plugins.sparql.processor import processUpdate
from rdflib.plugins.sparql.sparql import QueryContext
from pprint import pprint
from oc_ocdm.graph import GraphSet
from oc_ocdm.prov import ProvSet
from oc_ocdm import Storer, Reader
import sys, rdflib, pytz
from datetime import datetime
from oc_ocdm.graph.entities.identifier import Identifier
from oc_ocdm.graph.entities.bibliographic import AgentRole

from time_agnostic_browser.sparql import Sparql
from time_agnostic_browser.prov_entity import ProvEntity
from time_agnostic_browser.agnostic_entity import AgnosticEntity
from time_agnostic_browser.agnostic_query import AgnosticQuery


query = f"""
SELECT DISTINCT ?s
WHERE {{
    <https://github.com/arcangelo7/time_agnostic/ar/1> <{AgentRole.iri_is_held_by}> ?o.
}}
"""
# agnostic_query = AgnosticQuery(query=query)
# agnostic_query = AgnosticQuery(past_graphs_location="http://localhost:19999/blazegraph/sparql", query=query)
agnostic_query = AgnosticQuery(past_graphs_destination="http://localhost:19999/blazegraph/sparql", query=query)
# agnostic_query = AgnosticQuery(past_graphs_location="past_graphs.json", query=query)

# results = agnostic_query.run_agnostic_query()
# pprint(results)
                            
