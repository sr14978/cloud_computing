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
    url,name = storage.upload_file(f, f.filename)
    publish = queue.get_publisher('breakup')
    data = json.dumps({'messages': [{'attributes': {'type': 'breakup', 'flags': flags}, 'data': name}]})
    publish(data=data);
    return "OK", 200
    
app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api/v1')
