import json

from flask import Flask, request, make_response, jsonify
from screenshot import take_screenshot
app = Flask("get-screenshot")

POST = "POST"
URL = "url"
URLS = "urls"


@app.before_request
def only_json():
    if request.method == POST and not request.is_json:
        return "not json", 400

@app.route("/screenshot", methods=[POST])
def get_screenshot():
    rjson = request.json

    # check if it's a list or one link
    if URL not in rjson.keys() and URLS not in rjson.keys():
        return jsonify({"message": "invalid request"}), 400

    # one link: return the url
    if URL in rjson:
        return jsonify({"screenshot": take_screenshot(rjson[URL])}), 200

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
