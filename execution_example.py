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
from time_agnostic_browser.agnostic_query import AgnosticQuery, BlazegraphQuery


query = """
    prefix cito: <http://purl.org/spar/cito/>
    prefix datacite: <http://purl.org/spar/datacite/>
    prefix literal: <http://www.essepuntato.it/2010/06/literalreification/>
    select distinct ?elt_1
    where {
        ?elt_1 datacite:hasIdentifier ?id_1;
            datacite:hasIdentifier ?id_2.
        ?id_1 literal:hasLiteralValue ?literal_1.
        ?id_2 literal:hasLiteralValue ?literal_2.
        FILTER (?literal_1 != ?literal_2)
    }     
"""
agnostic_query = BlazegraphQuery(query, entity_types={"http://purl.org/spar/fabio/JournalArticle"}, config_path="config.json")
# output = agnostic_query.run_agnostic_query()
# pprint(output)

                            
