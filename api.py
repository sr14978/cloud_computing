from flask import Flask, Blueprint, request
import queue
import storage
import json
api = Blueprint('api_blueprint', __name__)

recv_messages = []
@api.route("/")
def home():
    return str(recv_messages)
    
@api.route("/submit", methods=['PUT'])
def submit():
    f = request.files['source.zip']
    flags = request.form['flags']
    recv_messages.append(str(f))
    safe_filename = storage.safe_filename(f.filename)
    storage.upload_file(f, safe_filename)
    publish = queue.get_publisher('worker')
    data = json.dumps({'messages': [{'attributes': {'type': 'unzip', 'flags': flags}, 'data': safe_filename}]})
    publish(data=data);
    return "OK", 200
    
app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api/v1')
