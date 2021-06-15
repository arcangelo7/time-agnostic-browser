from flask import Flask, render_template, request, jsonify, session

from time_agnostic_browser.agnostic_entity import AgnosticEntity
from time_agnostic_browser.agnostic_query import AgnosticQuery
from time_agnostic_browser.support import FileManager, _to_nt_sorted_list, _to_dict_of_nt_sorted_lists
from time_agnostic_browser.sparql import Sparql

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

@app.route("/")
def home():
    return render_template("home.jinja2")

@app.route("/entity/<path:res>")
def entity(res):
    agnostic_entity = AgnosticEntity(res=res, related_entities_history=False)
    try:
        history = agnostic_entity.get_history()
        history = _to_dict_of_nt_sorted_lists(history)
        for uri, snapshots in history.items():
            for snapshot in list(snapshots):
                triples = history[uri].pop(snapshot)
                decoded_triples = [decode_html(triple) for triple in triples]
                history[uri][snapshot] = decoded_triples
        return render_template("entity.jinja2", res=res, history=history)
    except Exception as e:
        print(e)
        return jsonify({'results': 'error'})

if __name__ == "__main__":
    app.run(debug=True)