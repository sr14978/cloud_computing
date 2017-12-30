from flask import Flask, Blueprint, request
import queue
import storage
api = Blueprint('api_blueprint', __name__)

messages = []
@api.route("/")
def home():
    return str(messages)
    
@api.route("/submit", methods=['PUT'])
def submit():
    f = request.files['source.zip']
    messages.append(str(f))
    url,name = storage.upload_file(f)
    publish = queue.get_publisher('breakup')
    publish(data='{"messages": [{"attributes": {"type": "breakup"}, "data": "' + name + '" } ]}');
    return "OK", 200

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api/v1')
