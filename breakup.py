from flask import Flask, Blueprint, request
import json
import base64
import storage
import random
import os
breakup = Blueprint('breakup_blueprint', __name__)
import shutil


messages = []
@breakup.route("/", methods=['POST'])
def job():
    envelope = json.loads(request.data.decode('utf-8'))
    payload = base64.b64decode(envelope['message']['data'])
    
    message = payload['messages'][0]
    if message['attributes']['type'] == 'breakup':
        return breakup_step(message['data'])
    elif message['attributes']['type'] == 'compile':
        return compile_step(message['data'])
    elif message['attributes']['type'] == 'link':
        return 'Ok', 200 # Not implemented yet

@breakup.route("/get")
def get():
    return str(messages)
    
app = Flask(__name__)
app.register_blueprint(breakup, url_prefix='/_ah/breakup')

def breakup_step(blob_name):
    messages.append(blob_name)
    rand = str(random.getrandbits(128))
    zip_filepath = '/tmp/source-' + rand + '.zip'
    with open(zip_filepath, 'wb') as zip_file:
        storage.download_file(blob_name, zip_file)
        
    folder_out_path = '/tmp/' + rand + '-unpacked'
    unzip(zip_filepath, folder_out_path)  
    os.remove(zip_filepath)
    
    publish = queue.get_publisher('breakup')
    for source_file_name in os.listdir(folder_out_path):
        with open(folder_out_path + '/' + source_file_name, 'r') as source_file:
            url, safe_filename = storage.upload_file(source_file)
            publish(data='{"messages": [{"attributes": {"type": "compile"}, "data": "' + safe_filename + '" } ]}')
    shutil.rmtree(folder_out_path)
    
    storage.delete_file(blob_name)
    
    return 'Ok', 200

def unzip(zip_in_path, folder_out_path):
    with zipfile.ZipFile(zip_in_path) as z:
        z.extractall(folder_out_path)
    

def compile_step(blob_name):
    messages.append(blob_name)
    source_file_path = '/tmp/' + blob_name
    with open(source_file_path, 'wb') as source_file:
        storage.download_file(blob_name, source_file)
    
    object_file_path = '/tmp/' + blob_name.rsplit('.', 1)
    compile(source_file_path, object_file_path)
    os.remove(source_file_path)
    
    publish = queue.get_publisher('breakup')
    with open(object_file_path, 'r') as object_file:
        url, safe_filename = storage.upload_file(object_file)
        publish(data='{"messages": [{"attributes": {"type": "link"}, "data": "' + safe_filename + '" } ]}')
        
    os.remove(object_file_path)
    storage.delete_file(blob_name)
    
    return 'Ok', 200
    
def compile(source_file_path, object_file_path):
    shutil.copyfile(source_file_path, object_file_path) ##TODO replace with compilation
    pass
