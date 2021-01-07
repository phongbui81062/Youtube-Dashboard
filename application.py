from flask import Flask
from flask_cors import CORS
from waitress import serve
from app import api_bp


app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api')
CORS(app)


if __name__ == '__main__':
    serve(app, listen="127.0.0.1:5000", threads=4)
