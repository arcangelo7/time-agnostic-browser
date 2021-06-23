from flask import Flask, render_template, request, jsonify, session
from collections import OrderedDict
from dateutil import parser
from SPARQLWrapper import SPARQLWrapper, JSON

from time_agnostic_browser.agnostic_entity import AgnosticEntity
from time_agnostic_browser.agnostic_query import AgnosticQuery
from time_agnostic_browser.support import FileManager, _to_nt_sorted_list, _to_dict_of_nt_sorted_lists
from time_agnostic_browser.sparql import Sparql

from pprint import pprint

app = Flask(__name__)

def decode_html(string:str) -> str:
    map = {
        '&': '&#38;',
        '<': '&#60;',
        '>': '&#62;',
        '"': '&#34;',
        "'": '&#039;',
        "/": "&#47;"
    }
    decoded_string = "".join([map[char] if char in map else char for char in string])
    return decoded_string

def human_readable_date(date:str) -> str:
    datetime_obj = parser.parse(date).replace(tzinfo=None)
    return str(datetime_obj)

@app.route("/")
def home():
    return render_template("home.jinja2")

@app.route("/entity/<path:res>")
def entity(res):
    agnostic_entity = AgnosticEntity(res=res, related_entities_history=False)
    try:
        history = agnostic_entity.get_history()
        history = _to_dict_of_nt_sorted_lists(history)
        human_readable_history = dict()
        for uri, snapshots in history.items():
            sorted_snapshots = sorted(
                snapshots.items(),
                key=lambda x: parser.parse(x[0]),
                reverse=True
            )
            for snapshot, triples in sorted_snapshots:
                decoded_triples = [triple.replace("<", "").replace(">", "") for triple in triples]
                human_readable_snapshot = human_readable_date(snapshot)
                human_readable_history.setdefault(uri, dict())
                human_readable_history[uri][human_readable_snapshot] = decoded_triples
        if len(human_readable_history):
            return render_template("entity.jinja2", res=res, history=human_readable_history)
        else:
            return jsonify({'results': None})
    except Exception as e:
        print(e)
        return jsonify({'results': 'error'})

@app.route("/is_an_entity/<path:res>")
def is_an_entity(res):
    agnostic_entity = AgnosticEntity(res=res, related_entities_history=False)
    try:
        history = agnostic_entity.get_history()
        history = _to_dict_of_nt_sorted_lists(history)
        human_readable_history = dict()
        for uri, snapshots in history.items():
            sorted_snapshots = sorted(
                snapshots.items(),
                key=lambda x: parser.parse(x[0]),
                reverse=True
            )
            for snapshot, triples in sorted_snapshots:
                decoded_triples = [triple.replace("<", "").replace(">", "") for triple in triples]
                human_readable_snapshot = human_readable_date(snapshot)
                human_readable_history.setdefault(uri, dict())
                human_readable_history[uri][human_readable_snapshot] = decoded_triples
        if len(human_readable_history):
            # return render_template("entity.jinja2", res=res, history=human_readable_history)
            return jsonify({'results': human_readable_history})
        else:
            return jsonify({'results': None})
    except Exception as e:
        print(e)
        return jsonify({'results': 'error'})

if __name__ == "__main__":
    app.run(debug=True)