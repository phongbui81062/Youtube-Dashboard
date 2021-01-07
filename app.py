from flask import Blueprint
from flask_restful import Resource, Api


class HelloWorld(Resource):
    def get(self):
        return {"Greeting": 'Hello World'}


api_bp = Blueprint('api', __name__)
api = Api(api_bp)
api.add_resource(HelloWorld, '/Greeting/')
