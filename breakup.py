from flask import Flask, Blueprint, request

breakup = Blueprint('breakup_blueprint', __name__)
    
messages = []
@breakup.route("/")
def job():
    data = json.loads(request.data.decode('utf-8'))
    messages.append(data)
    return 200

@breakup.route("/get")
def get():
    return messages.append(data).encode('utf-8')
    
app = Flask(__name__)
app.register_blueprint(breakup, url_prefix='/_ah/breakup')
