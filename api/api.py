from flask import Flask, Blueprint

api = Blueprint('api_blueprint', __name__)

@api.route("/")
def api_home():
    return "api home"
    

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api/v1')
