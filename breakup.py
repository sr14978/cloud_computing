from flask import Flask, Blueprint, request
import json
breakup = Blueprint('breakup_blueprint', __name__)
    
messages = []
@breakup.route("/", methods=['POST'])
def job():
    data = json.loads(request.data.decode('utf-8'))
    messages.append(data)
    return 'Ok', 200

@breakup.route("/get")
def get():
    return str(messages)
    
app = Flask(__name__)
app.register_blueprint(breakup, url_prefix='/_ah/breakup')
