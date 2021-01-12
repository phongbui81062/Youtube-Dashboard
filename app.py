from flask import Blueprint
from flask_restful import Resource, Api
from resource.get_comment import Comment


class HelloWorld(Resource):
    def get(self):
        return {"Greeting": 'Hello World'}


api_bp = Blueprint('api', __name__)
api = Api(api_bp)
api.add_resource(HelloWorld, '/Greeting/')
api.add_resource(Comment, '/Comment/')