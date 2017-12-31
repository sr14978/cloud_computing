from flask import Flask, send_file, Blueprint, request
app = Flask(__name__)
@app.route("/static/index.html")
def index():
    return send_file('index.html')
    
@app.route("/static/css/index.css")
def css():
    return send_file('css/index.css')
    
@app.route("/static/scripts/index.js")
def js():
    return send_file('scripts/index.js')
    
api = Blueprint('api_blueprint', __name__)

messages = []
@api.route("/")
def home():
    return str(messages)
    
@api.route("/submit", methods=['PUT'])
def submit():
    zip = request.files['source.zip']
    flags = request.form['flags']
    print(zip.filename)
    print(flags)
    messages.append(str(f))
    return "OK", 200

app.register_blueprint(api, url_prefix='/api/v1')