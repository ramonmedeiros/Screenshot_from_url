import json
import threading

from flask import Flask, request, make_response, jsonify
from flask_restplus import Api, Resource, fields
from screenshot import take_screenshot

app = Flask("get-screenshot")
api = Api (app = app)

namespace = api.namespace("/", description="Screenshot as a Service")

URL = "url"
POST = "POST"
URLS = "urls"

lock = threading.Lock()

@namespace.route("/screenshot")
class Screenshot(Resource):
    resource_fields = api.model('Screenshot', {
        'url': fields.Url,
    })

    @api.expect(resource_fields)
    def post(self):
        if request.method == POST and not request.is_json:
            return "not json", 400

        rjson = request.json

        # check if it's a list or one link
        if URL not in rjson.keys():
            return jsonify({"message": "invalid request"}), 400

        url = rjson[URL]

        # don't do screenshot in paralel
        with lock:
            screenshotUrl = take_screenshot(url)

        return jsonify({"screenshot": screenshotUrl})

@namespace.route("/screenshots")
class Screenshots(Resource):
    resource_fields = api.model('Screenshots', {
        'urls': fields.Url,
    })

    @api.expect(resource_fields)
    def post(self):

        if request.method == POST and not request.is_json:
            return "not json", 400

        rjson = request.json

        # check if it's a list or one link
        if URLS not in rjson.keys():
            return jsonify({"message": "invalid request"}), 400

        # multiple links: split list, report if some error is found, return with a list
        if URLS in rjson:
            screenshots = []
            urls = rjson.get(URLS).split(";")

            if len(urls) == 0:
                return jsonify({"message": "expected urls separated by ;"}), 400

            for url in urls:
                with lock:
                    screenshots.append({url: take_screenshot(url)})

            return jsonify({"screenshots": screenshots})

        return jsonify({"message": "invalid request"}), 400

