from flask import Flask, Blueprint, request
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from pubsub import pubsub
api = Blueprint('api_blueprint', __name__)

@api.route("/")
def home():
    return "api home"
    
@api.route("/submit", methods=['PUT'])
def submit():
    f = request.files['source.zip']
    pubsub.add_breakup_job(b'job')
    return 200

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api/v1')
