from flask import Flask, Blueprint, request
import json
import base64
breakup = Blueprint('breakup_blueprint', __name__)
    
messages = []
@breakup.route("/", methods=['POST'])
def job():
    envelope = json.loads(request.data.decode('utf-8'))
    payload = base64.b64decode(envelope['message']['data'])
    messages.append(payload)
    return 'Ok', 200

@breakup.route("/get")
def get():
    return str(messages)
    
app = Flask(__name__)
app.register_blueprint(breakup, url_prefix='/_ah/breakup')
