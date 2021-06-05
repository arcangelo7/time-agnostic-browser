from SPARQLWrapper import XML, SPARQLWrapper, JSON, POST
from SPARQLWrapper.Wrapper import RDFXML
from rdflib import URIRef, Literal, Graph, ConjunctiveGraph
from rdflib.plugins.sparql import sparql
from rdflib.plugins.sparql.processor import processUpdate
from rdflib.plugins.sparql.sparql import QueryContext
from pprint import pprint
import sys
import rdflib

from time_agnostic_browser.sparql import Sparql
from time_agnostic_browser.agnostic_query import AgnosticQuery
from time_agnostic_browser.agnostic_entity import AgnosticEntity, get_entities_histories
from time_agnostic_browser.support import FileManager, _to_dict_of_nt_sorted_lists, _to_nt_sorted_list

query = """
select ?citedEntity
where {
    ?s ?p ?o;
        <http://purl.org/spar/cito/cites> ?citedEntity.
    BIND (<https://github.com/arcangelo7/time_agnostic/br/1> as ?s).
}
"""
agnostic_query = AgnosticQuery(past_graphs_location="past_graphs.json", query=query)
agnostic_result = agnostic_query.run_agnostic_query()
pprint(agnostic_result)

