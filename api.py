from flask import Flask, Blueprint, request
import queue
api = Blueprint('api_blueprint', __name__)

messages = []
@api.route("/")
def home():
    return str(messages)
    
@api.route("/submit", methods=['PUT'])
def submit():
    f = request.files['source.zip']
    messages.append(str(f))
    publish = queue.get_publisher('breakup')
    publish(data='{"messages": [{"attributes": {"type": "breakup"}, "data": "<path_to_zip_on_blob>" } ]}')
    return "OK", 200

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api/v1')
