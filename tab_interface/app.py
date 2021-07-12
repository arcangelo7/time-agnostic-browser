from typing import Dict, List, Tuple
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from rdflib.plugins.sparql.processor import prepareQuery
from collections import OrderedDict
from dateutil import parser
from SPARQLWrapper import SPARQLWrapper, JSON
import urllib

from time_agnostic_browser.agnostic_entity import AgnosticEntity
from time_agnostic_browser.agnostic_query import AgnosticQuery, BlazegraphQuery, CONFIG_PATH
from time_agnostic_browser.support import FileManager, _to_nt_sorted_list, _to_dict_of_nt_sorted_lists
from time_agnostic_browser.sparql import Sparql

from pprint import pprint

CONFIG_PATH = "./tab_interface/config.json"

app = Flask(__name__)
app.secret_key = b'\x94R\x06?\xa4!+\xaa\xae\xb2\xf3Z\xb4\xb7\xab\xf8'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
config = FileManager(CONFIG_PATH).import_json()
rules:Dict[str, Dict] = config["rules_on_properties_order"]

def get_human_readable_date(date:str) -> str:
    datetime_obj = parser.parse(date).replace(tzinfo=None)
    return datetime_obj.strftime("%d %B %Y, %H:%M:%S")

def get_type_of_entity(snapshots:Dict[str, List[str]]) -> str:
    for _, triples in snapshots.items():
        for triple in triples:
            if "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" in triple:
                type_of_entity = triple.split()[-1].replace("<", "").replace(">", "")
                return type_of_entity

def sort_by_time(snapshots:Dict[str, Dict]) -> List[Tuple[str, Dict]]:
    sorted_snapshots = sorted(
        snapshots.items(),
        key=lambda x: parser.parse(x[0]),
        reverse=True
    )
    return sorted_snapshots

def get_human_readable_history(history:dict) -> dict:
    history = _to_dict_of_nt_sorted_lists(history)
    human_readable_history = dict()
    for uri, snapshots in history.items():
        sorted_snapshots = sort_by_time(snapshots)
        type_of_entity = get_type_of_entity(snapshots)
        for snapshot, triples in sorted_snapshots:
            list_of_lists = list()
            for triple in triples:
                literal = triple.split('"')
                s_p = literal[0].replace("<", "").replace(">", "").split()
                s = s_p[0]
                p = s_p[1]
                o = literal[1].replace('"', '') if len(literal) > 1 else s_p[2]
                list_of_lists.append([s, p, o])
            if type_of_entity in rules:
                list_of_lists = (sorted(list_of_lists, key=lambda triple: 
                    rules[type_of_entity].get(triple[1], ord(triple[1].split("/")[-1].split("#")[-1][0]))))
            human_readable_snapshot = get_human_readable_date(snapshot)
            human_readable_history.setdefault(uri, dict())
            human_readable_history[uri][human_readable_snapshot] = list_of_lists
    return human_readable_history

def get_prov_metadata_by_time(prov_metadata:Dict[str, Dict]) -> Dict[str, Dict]:
    prov_metadata_by_time:Dict[str, Dict] = dict()
    for entity, snapshots in prov_metadata.items():
        for _, metadata in snapshots.items():
            prov_metadata_by_time.setdefault(entity, dict())
            time = get_human_readable_date(metadata["http://www.w3.org/ns/prov#generatedAtTime"])
            responsible_agent = metadata["http://www.w3.org/ns/prov#wasAttributedTo"]
            source = metadata["http://www.w3.org/ns/prov#hadPrimarySource"]
            description = metadata["http://purl.org/dc/terms/description"]
            prov_metadata_by_time[entity].setdefault(time, dict())
            prov_metadata_by_time[entity][time]["http://www.w3.org/ns/prov#generatedAtTime"] = time
            prov_metadata_by_time[entity][time]["http://www.w3.org/ns/prov#wasAttributedTo"] = responsible_agent
            prov_metadata_by_time[entity][time]["http://www.w3.org/ns/prov#hadPrimarySource"] = source
            prov_metadata_by_time[entity][time]["http://purl.org/dc/terms/description"] = description
    return prov_metadata_by_time

@app.route("/")
def home():
    return render_template("home.jinja2")

@app.route("/entity/<path:res>")
def entity(res):
    agnostic_entity = AgnosticEntity(res=res, related_entities_history=False)
    try:
        history = agnostic_entity.get_history(include_prov_metadata=True)
    except urllib.error.URLError:
        flash("There are connection problems with the database.")
        return redirect(url_for("home"))
    human_readable_history = get_human_readable_history(history[0])
    if human_readable_history:
        prov_metadata = get_prov_metadata_by_time(history[1])
        return render_template("entity.jinja2", res=res, history=human_readable_history, prov_metadata=prov_metadata)
    else:
        flash("I do not have information about that entity in my data.")
        return redirect(request.referrer)

@app.route("/query", methods = ['POST'])
def query():
    query = request.form.get("query")
    agnostic_query = BlazegraphQuery(query)
    agnostic_results = agnostic_query.run_agnostic_query()
    variables = prepareQuery(query).algebra["PV"]
    agnostic_results = sort_by_time(agnostic_results)
    response = list()
    for se, outputs in agnostic_results:
        time = get_human_readable_date(se)
        response.append({time: list()})
        for output in outputs:
            var_to_values = dict()
            for i, el in enumerate(output):
                var = str(variables[i])
                var_to_values[var] = el
            dict_to_update:Dict[str, list] = next(item for item in response if time in item.keys())
            dict_to_update[time].append(var_to_values)
    return jsonify(response=response)

@app.route("/get_config")
def get_config():
    return jsonify(config)

if __name__ == "__main__":
    app.run(debug=True)