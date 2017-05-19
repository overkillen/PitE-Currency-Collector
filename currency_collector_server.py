from flask import Flask
from flask import request
import flask
import json
import argparse


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
    def generate_response_for_the_same_currencies(currency):
        return JsonResponse(json.dumps({currency:1})).prepare_response()

    @staticmethod
    @app.route("/")
    def index():
        return "Currency Collector Server"

    @staticmethod
    def run_server(port_to_listen):
        RestServer.app.run(host='0.0.0.0', port=port_to_listen)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Runs currency collector')
    argparser.add_argument('--port', dest='port', default=5000)
    args = argparser.parse_args()

    server = RestServer()
    server.run_server(args.port)