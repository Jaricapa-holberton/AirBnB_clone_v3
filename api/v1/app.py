#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)

"""@app.route('/', strict_slashes=False)
def index():
    return 'Hello HBNB!'"""


@app.errorhandler(404)
def handle_404(error):
    """returns json 404 status code response"""
    return (jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    host = os.getenv("HBNB_API_HOST")
    port = os.getenv("HBNB_API_PORT")
    if not host:
        host = '0.0.0.0'
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
