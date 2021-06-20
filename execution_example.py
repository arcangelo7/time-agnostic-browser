from datetime import time
from SPARQLWrapper import XML, SPARQLWrapper, JSON, POST
from SPARQLWrapper.Wrapper import RDFXML
from oc_ocdm.graph.graph_entity import GraphEntity
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


query = """
    prefix literal: <http://www.essepuntato.it/2010/06/literalreification/>
    prefix datacite: <http://purl.org/spar/datacite/>
    prefix pro: <http://purl.org/spar/pro/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT DISTINCT ?o ?id ?value
    WHERE {
        <https://github.com/arcangelo7/time_agnostic/ar/15519> pro:isHeldBy ?o;
        OPTIONAL {<https://github.com/arcangelo7/time_agnostic/ar/15519> rdf:type pro:RoleInTime.}
        ?o datacite:hasIdentifier ?id.
        ?id literal:hasLiteralValue ?value.
    }
""" 
# agnostic_query = AgnosticQuery(query=query)
# agnostic_query = AgnosticQuery(past_graphs_location="http://localhost:19999/blazegraph/sparql", query=query)
agnostic_query = AgnosticQuery(query=query)
# results = agnostic_query.run_agnostic_query()
# pprint(results)
# agnostic_query = AgnosticQuery(past_graphs_location="past_graphs.json", query=query)

# results = agnostic_query.run_agnostic_query()
# pprint(results)
                            
