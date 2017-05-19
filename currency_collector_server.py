from flask import Flask
import flask
import requests
import argparse
from tinydb import TinyDB, Query
import thread
import time

db = TinyDB('currency_base.json')


def update_db():
    while True:
        time.sleep(10)
        db.insert(requests.get("http://api.fixer.io/2016-03-03").json())
        db.insert(requests.get("http://api.fixer.io/2016-03-03").json())
        db.insert(requests.get("http://api.fixer.io/2016-03-03").json())


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
        return JsonResponse(db.all()).prepare_response()

    @staticmethod
    def run_server(port_to_listen):
        RestServer.app.run(host='0.0.0.0', port=port_to_listen)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Runs currency collector')
    argparser.add_argument('--port', dest='port', default=5000)
    args = argparser.parse_args()
    thread.start_new_thread(update_db())
    server = RestServer()
    server.run_server(args.port)