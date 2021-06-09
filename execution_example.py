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
import sys
import rdflib
from oc_ocdm.graph.entities.identifier import Identifier

from time_agnostic_browser.sparql import Sparql
from time_agnostic_browser.prov_entity import ProvEntity
from time_agnostic_browser.agnostic_entity import AgnosticEntity


agnostic_entity = AgnosticEntity(res="https://github.com/arcangelo7/time_agnostic/id/1")
state_at_time = agnostic_entity.get_state_at_time(time="2021-06-04T09:36:53.000Z", get_hooks=True)
pprint(state_at_time)

                            
