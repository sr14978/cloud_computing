from flask import Flask, Blueprint, request
import json
import base64
import queue
import storage
import random
import os
import shutil
worker = Blueprint('worker_blueprint', __name__)
import unzipper
import compiler
import linker

messages = []
@worker.route("/", methods=['POST'])
def job():
    envelope = json.loads(request.data.decode('utf-8'))
    payload = base64.b64decode(envelope['message']['data'])
    
    message = json.loads(payload.decode('utf-8'))['messages'][0]
    if message['attributes']['type'] == 'unzip':
        return breakup_step(message)
    elif message['attributes']['type'] == 'compile':
        return compile_step(message)
    elif message['attributes']['type'] == 'link':
        return link_step(message)

@worker.route("/get")
def get():
    return str(messages)
    
app = Flask(__name__)
app.register_blueprint(worker, url_prefix='/_ah/worker')

def breakup_step(message):
    blob_name = message['data']
    messages.append(blob_name)
    rand = str(random.getrandbits(128))
    zip_filepath = '/tmp/source-' + rand + '.zip'
    with open(zip_filepath, 'wb') as zip_file:
        storage.download_file(blob_name, zip_file)
        
    folder_out_path = '/tmp/' + rand + '-unpacked'
    sources = unzipper.unzip(zip_filepath, folder_out_path)  
    os.remove(zip_filepath)
    
    publish = queue.get_publisher('worker')
    for source_file_name in sources:
        with open(folder_out_path + '/' + source_file_name, 'r') as source_file:
            url, safe_filename = storage.upload_file(source_file, source_file_name)
            data = json.dumps({'messages': [{'attributes': {'type': 'compile', 'flags': message['attributes']['flags']}, 'data': safe_filename}]})
            publish(data=data)
    shutil.rmtree(folder_out_path)
    
    storage.delete_file(blob_name)
    
    return 'Ok', 200

def compile_step(message):
    blob_name = message['data']
    
    messages.append(blob_name)
    source_file_path = '/tmp/' + blob_name
    with open(source_file_path, 'wb') as source_file:
        storage.download_file(blob_name, source_file)
        
    flags = json.loads(message['attributes']['flags'])
    object_file_path, msgs = compiler.compile(source_file_path, flags['compiler'], flags['compiler-flags'])
    os.remove(source_file_path)
    
    publish = queue.get_publisher('worker')
    with open(object_file_path, 'r') as object_file:
        object_file_name = object_file_path.rsplit('/',1)[-1]
        url, safe_filename = storage.upload_file(object_file, object_file_name)
        data = json.dumps({'messages': [{'attributes': {'type': 'link', 'flags': message['attributes']['flags'], 'msgs': msgs}, 'data': safe_filename}]})
        publish(data=data)
        
    os.remove(object_file_path)
    storage.delete_file(blob_name)
    
    return 'Ok', 200
    
def link_step(message):
    blob_name = message['data']
    flags = json.loads(message['attributes']['flags'])
    #linker.link(flags['exename'], flags['compiler'], flags['linker-flags'])
    return 'Ok', 200
    
    