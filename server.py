from flask import Flask, send_file, Blueprint, request, render_template, redirect, session
import json
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

@app.route("/")
def slash():
    if 'user_id' in session:
        return redirect('/loggedin')
    else:
        return redirect('/static/index.html')

@app.route("/loggedin")
def loggedin():
    if 'user_id' in session:
        return render_template('index.html', name='Sam Rusell')
    else:
        session['user_id'] = '1'
        return redirect('/static/index.html')

        
@app.route("/static/index.html")
def index():
    return send_file('static/index.html')

@app.route("/static/index.xhtml")
def xindex():
    return send_file('static/index.xhtml')    

@app.route("/static/css/index.css")
def css():
    return send_file('static/css/index.css')
    
@app.route("/static/scripts/index.js")
def js():
    return send_file('static/scripts/index.js')
    
@app.route("/history/index.html")
def history():
    return render_template('history.html',
    executables=[
      {'url':'24345123213', 'name':'fred', 'success': True},
      {'url':'34534345234', 'name':'pete', 'success': False},
      {'url':'12345234545213', 'name':'max', 'success': True},
      {'url':'314434323213', 'name':'alice', 'success': False}],
    name='Sam Rusell'  
      )
    
@app.route("/static/scripts/history.js")
def historyjs():
    return send_file('static/scripts/history.js')
    
@app.route("/static/css/history.css")
def historycss():
    return send_file('static/css/history.css')
  
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
    ret = {
      'success': True,
      'messages': ["warning: your code is shit", "only joking: you are maze"],
      'executable_name': "a.out"
    }
    return json.dumps(ret), 200

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