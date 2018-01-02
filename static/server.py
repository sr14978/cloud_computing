from flask import Flask, send_file, Blueprint, request
import json
import io

app = Flask(__name__)
@app.route("/static/index.html")
def index():
    return send_file('index.html')

@app.route("/static/index.xhtml")
def xindex():
    return send_file('index.xhtml')    

@app.route("/static/css/index.css")
def css():
    return send_file('css/index.css')
    
@app.route("/static/scripts/index.js")
def js():
    return send_file('scripts/index.js')
  
api = Blueprint('api_blueprint', __name__)

@api.route("/submit", methods=['PUT'])
def submit():
    zip = request.files['source.zip']
    compiler = request.form['compiler']
    compiler_flags = request.form['compiler-flags']
    linker_flags = request.form['linker-flags']
    flags = {
      'compiler': compiler,
      'exename': 'a.out',
      'compiler-flags': compiler_flags,
      'linker-flags': linker_flags
    }
    
    print(zip.filename)
    print(json.dumps(flags))
    return "23452345234", 200
    
ready_count = 0
@api.route("/ready/<rand>", methods=['GET'])
def ready(rand):
    global ready_count
    ready_count = ready_count + 1
    if ready_count == 5:
      ready_count = 0
      return "True", 200
    else:
      return "False", 200
    
@api.route("/results/<rand>", methods=['GET'])
def results(rand):
    return "Messages from server", 200

@api.route("/executable/<rand>", methods=['GET'])
def executable(rand):
    executable_name = "a.out"
    strIO = io.StringIO()
    strIO.write("this is the executable file")
    strIO.seek(0)
    return send_file(strIO,
                     attachment_filename=executable_name,
                     as_attachment=True), 200
    
app.register_blueprint(api, url_prefix='/api/v1')


"""
run by 
pip install flask

export['set' on windows] FLASK_APP=server.py
python -m flask run
"""