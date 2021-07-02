from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from collections import OrderedDict
from dateutil import parser
from SPARQLWrapper import SPARQLWrapper, JSON
import urllib

from time_agnostic_browser.agnostic_entity import AgnosticEntity
from time_agnostic_browser.agnostic_query import AgnosticQuery
from time_agnostic_browser.support import FileManager, _to_nt_sorted_list, _to_dict_of_nt_sorted_lists
from time_agnostic_browser.sparql import Sparql

from pprint import pprint

app = Flask(__name__)
app.secret_key = b'\x94R\x06?\xa4!+\xaa\xae\xb2\xf3Z\xb4\xb7\xab\xf8'

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
    except urllib.error.URLError:
        flash("There are connection problems with the database.")
        return redirect(url_for("home"))
    history = _to_dict_of_nt_sorted_lists(history)
    human_readable_history = dict()
    for uri, snapshots in history.items():
        sorted_snapshots = sorted(
            snapshots.items(),
            key=lambda x: parser.parse(x[0]),
            reverse=True
        )
        for snapshot, triples in sorted_snapshots:
            list_of_lists = list()
            for triple in triples:
                literal = triple.split('"')
                s_p = literal[0].replace("<", "").replace(">", "").split()
                s = s_p[0]
                p = s_p[1]
                o = literal[1].replace('"', '') if len(literal) > 1 else s_p[2]
                list_of_lists.append([s, p, o])
            human_readable_snapshot = human_readable_date(snapshot)
            human_readable_history.setdefault(uri, dict())
            human_readable_history[uri][human_readable_snapshot] = list_of_lists
    if human_readable_history:
        return render_template("entity.jinja2", res=res, history=human_readable_history)
    else:
        flash("I do not have information about that in my data.")
        return redirect(request.referrer)

if __name__ == "__main__":
    app.run(debug=True)