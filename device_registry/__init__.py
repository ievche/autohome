import markdown
import os
import redis
import json
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

def get_redis():
   r = redis.Redis(host='redis-server', port=6379, db=0)
   return r

@app.route("/")
def index():
    """Present Docs"""
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        content = markdown_file.read()

        return markdown.markdown(content)

class DeviceList(Resource):
    def get(self):
        r = get_redis()
        keys = r.keys()

        devices = []

        for key in keys:
            device = r.get(key).decode('utf8').replace("'", '"')
            device = json.loads(device)
            devices.append(device)

        return { 'message': 'Success', 'data': devices }

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('device_type', required=True)
        parser.add_argument('controller_gateway', required=True)

        args = parser.parse_args()

        r = get_redis()
        r.set(args['identifier'], str(args))

        return { 'message': 'Device registered', 'data': args }, 201

class Device(Resource):
    def get(self, identifier):
        r = get_redis()
        
        str_keys = []
        for key in r.keys():
            str_key = str(key, 'utf-8')
            str_keys.append(str_key)

        if not (identifier in str_keys):
            return {'message': 'Device not found', 'data': {}}, 404

        return {'message': 'Device found', 'data': str(r.get(identifier), 'utf-8')}, 200

    def delete(self, identifier):
        r = get_redis()

        str_keys = []
        for key in r.keys():
            str_key = str(key, 'utf-8')
            str_keys.append(str_key)

        
        if not (identifier in str_keys):
            return {'message': 'Device not found', 'data': {}}, 404

        r.delete(identifier)
        return '', 204

api.add_resource(Device, '/device/<string:identifier>')
api.add_resource(DeviceList, '/devices')
