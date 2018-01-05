from flask import Flask, Blueprint, request, send_file, session
import queue
import storage
import database
import json
import random
import StringIO
from google.api_core.exceptions import InvalidArgument

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xde{\xcb\xd0\x97gi\x9a\x9f\x18G\xb2\x18\xed8d\xd2\x9e[\xa4=\xf5\xac\xa4'

api = Blueprint('api_blueprint', __name__)

recv_messages = []
@api.route("/")
def home():
    return str(recv_messages)
    
@api.route("/submit", methods=['PUT'])
def submit():
    f = request.files['source.zip']
    compiler = request.form['compiler']
    compiler_flags = request.form['compiler-flags']
    linker_flags = request.form['linker-flags']
    flags = {
      'compiler': compiler,
      'exename': 'a.out',
      'compiler-flags': compiler_flags,
      'linker-flags': linker_flags
    }
    
    if not 'user_id' in session:
        return "User_id not available", 401
        
    user_id = session['user_id']
    print("user_id:", user_id)
    user = database.get_user(user_id)
    if user == None:
        return "Invalid user", 401
    
    recv_messages.append(str(f))
    safe_filename = storage.safe_filename(f.filename)
    storage.upload_file(f, safe_filename)
    
    try:
        publish = queue.get_publisher('worker')
    except InvalidArgument:
        return "Task queue not initialised", 500
    
    rand = str(random.getrandbits(128))
    data = json.dumps({
      'messages': [{
        'attributes': {
          'type': 'unzip',
          'flags': json.dumps(flags),
          'job_result_blobname': rand + "-job_result",
          'executable_blobname': rand + "-executable",
          'rand': rand,
          'user_id': user_id
        },
        'data': safe_filename
      }]
    })
    publish(data=data);   
    return rand, 200
    
@api.route("/ready/<rand>", methods=['GET'])
def ready(rand):
    return str(storage.file_exists(rand + "-job_result")), 200
    
@api.route("/results/<rand>", methods=['GET'])
def results(rand):
    if storage.file_exists(rand + "-job_result"):
        return storage.download_string(rand + "-job_result"), 200
    else:
        return "Not ready", 401

@api.route("/executable/<rand>", methods=['GET'])
def executable(rand):
    if storage.file_exists(rand + "-executable"):
        executable_name = json.loads(storage.download_string(rand + "-job_result"))['executable_name']
        strIO = StringIO.StringIO()
        strIO.write(storage.download_string(rand + "-executable"))
        strIO.seek(0)
        return send_file(strIO,
                         attachment_filename=executable_name,
                         as_attachment=True), 200
    else:
        return "Not ready", 401


@api.route("/user_id", methods=['GET'])
@oauth2.required
def get
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        return "User_id not available", 401
    user = database.get_user(user_id)
    if user != None:
        return json.dumps(user['executables']), 200
    else:
        return "Invalid user", 401
    

app.register_blueprint(api, url_prefix='/api/v1')
