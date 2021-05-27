import flask
from flask import request, jsonify


import json


from service import MakeService
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/v2/api/car/makes', methods=['GET'])
def getMakes():
    return json.dumps(MakeService.getAllMakes())
    # return json.dumps(foundItems(key))
    # return json.dumps([ob.__dict__ for ob in MakeService.getAllMakes()])




@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

app.run(host='0.0.0.0', port=9090)