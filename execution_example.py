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
    prefix cito: <http://purl.org/spar/cito/>
    prefix datacite: <http://purl.org/spar/datacite/>
    select distinct ?elt_1
    where {
        ?elt_1 datacite:hasIdentifier ?id_1;
                datacite:hasIdentifier ?id_2.
        <https://github.com/arcangelo7/time_agnostic/br/102437> cito:cites ?elt_1.
        FILTER (?id_1 != ?id_2)
    }
"""
agnostic_query = AgnosticQuery(query)

                            
