from flask import Flask, Blueprint, request

breakup = Blueprint('breakup_blueprint', __name__)
    
@breakup.route("/")
def job():
    return 200

app = Flask(__name__)
app.register_blueprint(breakup, url_prefix='/_ah/breakup')
