from flask import Flask, Blueprint, request
#from pubsub import pubsub
api = Blueprint('api_blueprint', __name__)

messages = []
@api.route("/")
def home():
    return str(messages)
    
@api.route("/submit", methods=['PUT'])
def submit():
    f = request.files['source.zip']
    messages.append(str(f))
    #pubsub.add_breakup_job(data='{"messages": [{"attributes": {"type": "breakup"}, "data": "<path_to_zip_on_blob>" } ]}')
    return "OK", 200

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api/v1')
