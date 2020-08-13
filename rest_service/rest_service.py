from flask import Flask, request
from handlers import upload_data_handler, download_data_handler


app = Flask(__name__)


@app.route('/v1/file/download/<int:key_value>', methods=['GET'])
def hello_world(key_value):
    return download_data_handler(key_value)


@app.route('/v1/file/upload', methods=['POST'])
def post_request():
    return upload_data_handler(request)


if __name__ == '__main__':
    app.run()
