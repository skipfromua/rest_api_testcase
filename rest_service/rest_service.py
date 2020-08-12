from flask import Flask, request, abort, jsonify
import json
from .dropbox_api import download, upload, dbx_object


app = Flask(__name__)


@app.route('/binary_file/<int:key_value>', methods=['GET'])
def hello_world(key_value):
    data = download(dbx_object, '{}.json'.format(key_value))
    print(data)
    return jsonify({key_value: data.decode('utf-8')})


@app.route('/binary_file', methods=['POST'])
def post_request():
    if not request.json:
        abort(400)
    print(request.json)
    upload(dbx_object, '{}.json'.format(request.json['key_value']), request.json['data'])
    return json.dumps(request.json)
