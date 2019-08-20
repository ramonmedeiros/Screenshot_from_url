import json
import threading
import time

from flask import Flask, request, make_response, jsonify
from flask_restplus import Api, Resource, fields
from pub import take_screenshot, RuntimeException, get_image_exists

app = Flask("get-screenshot")
api = Api(app=app)

namespace = api.namespace("/", description="Screenshot as a Service")

URL = "url"
POST = "POST"
URLS = "urls"


@api.errorhandler(RuntimeException)
def handle_invalid_usage(error):
    return {'message': error.message}, 400


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

        # take screenshot
        url = rjson[URL]
        ret = take_screenshot(url)

        # ret is a link: return
        if "url" in ret.keys():
            return jsonify({"screenshot": ret["url"]})

        # wait for screenshot
        for i in range(10):
            link = get_image_exists(ret["hash"])
            if len(link) > 0:
                break
            time.sleep(0.01)
 
        return jsonify({"screenshot": link})


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
                screenshots.append({url: take_screenshot(url)})

            return jsonify({"screenshots": screenshots})

        return jsonify({"message": "invalid request"}), 400
