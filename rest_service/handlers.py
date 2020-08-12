from .dropbox_api import download, upload, dbx_object
from flask import jsonify, json, abort


def download_data_handler(key_value):
    data = download(dbx_object, '{}'.format(key_value))
    return jsonify(data.decode('utf-8'))


def upload_data_handler(request):
    if request.headers['Content-Type'] == 'text/plain':
        hashed_data = abs(hash(request.data))
        upload(dbx_object, '{}'.format(hashed_data), request.data)
        return "200 Key-value:{}".format(hashed_data)

    elif request.headers['Content-Type'] == 'application/json':
        if not request.json:
            abort(400)
        upload(dbx_object, '{}'.format(request.json['key_value']), bytes(request.json['data'].encode()))
        return "200 JSON Message: " + json.dumps(request.json)

    elif request.headers['Content-Type'] == 'application/octet-stream':
        hashed_data = abs(hash(request.data))
        upload(dbx_object, '{}'.format(hashed_data), request.data)
        return "200 Key-value:{}".format(hashed_data)
    else:
        return "415 Unsupported Media Type ;)"
