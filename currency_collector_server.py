import argparse
import json
import threading
import time

import flask
import requests
from flask import Flask

import dropbox_stuff
from tinydb import TinyDB

db = TinyDB('currency_base.json')
dropbox_client = dropbox_stuff.DBClient()


def update_db():
    while True:
        db.insert(requests.get("http://www.apilayer.net/api/live?access_key=8f29723d2a727648269ba96a05b54dff").json())
        dropbox_client.upload_file(json.dumps(db.all()))
        time.sleep(3600)


class JsonResponse:
    json_content_type = "application/json"

    def __init__(self, data):
        self.data = data

    def prepare_response(self):
        response = flask.Response(self.data)
        response.headers['Content-Type'] = self.json_content_type
        return response


class RestServer:
    app = Flask("Currency Collector Server")


    @staticmethod
    @app.route("/")
    def index():
        return "Currency Collector Server"

    @staticmethod
    @app.route("/dump")
    def dump():
        content = json.dumps(db.all())
        dropbox_client.upload_file(content)
        return JsonResponse(content).prepare_response()

    @staticmethod
    def run_server(port_to_listen):
        RestServer.app.run(host='0.0.0.0', port=port_to_listen)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Runs currency collector')
    argparser.add_argument('--port', dest='port', default=5000)
    args = argparser.parse_args()
    # with open('currency_dump.json') as dump:
        # out = json.loads(dump.read())
        # for record in out:
            # db.insert(record)
    out = json.loads(dropbox_client.download_file())
    for record in out:
        db.insert(record)
    updater = threading.Thread(target=update_db)
    updater.daemon = True
    updater.start()
    server = RestServer()
    server.run_server(args.port)
