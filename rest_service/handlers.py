from .dropbox_api import download, upload, dbx_object
from flask import jsonify, json, abort


def download_data_handler(key_value):
    data = download(dbx_object, str(key_value))
    return jsonify(data.decode())


def upload_data_handler(request):
    if request.headers['Content-Type'] == 'text/plain':
        return "200 Key-value:{}".format(_text_plain_parse(request))

    elif request.headers['Content-Type'] == 'application/json':
        return "200 JSON Message: {}".format(_application_json_parse(request))

    elif request.headers['Content-Type'] == 'application/octet-stream':
        return "200 Key-value:{}".format(_application_octet_stream_parse(request))
    else:
        return "415 Unsupported Media Type ;)"


def _text_plain_parse(request):
    hashed_data = abs(hash(request.data))
    upload(dbx_object, '{}'.format(hashed_data), request.data)
    return hashed_data


def _application_json_parse(request):
    if not request.json:
        abort(400)
    upload(dbx_object, '{}'.format(request.json['key_value']), bytes(request.json['data'].encode()))
    return json.dumps(request.json)


def _application_octet_stream_parse(request):
    hashed_data = abs(hash(request.data))
    upload(dbx_object, '{}'.format(hashed_data), request.data)
    return hashed_data
