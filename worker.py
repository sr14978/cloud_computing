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
        return unzip_step(message)
    elif message['attributes']['type'] == 'compile':
        return compile_step(message)
    elif message['attributes']['type'] == 'link':
        return link_step(message)

@worker.route("/get")
def get():
    return str(messages)
    
app = Flask(__name__)
app.register_blueprint(worker, url_prefix='/_ah/worker')

def unzip_step(message):
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
    files = []
    for source_file_name in sources:
        with open(folder_out_path + '/' + source_file_name, 'r') as source_file:
            safe_source_file_name = storage.safe_filename(source_file_name)
            storage.upload_file(source_file, safe_source_file_name)
            file_attributes = {'filename': convert_sourcepath_to_objectpath(source_file_name), 'blob_name': convert_sourcepath_to_objectpath(safe_source_file_name)}
            files.append(file_attributes)
            data = json.dumps({'messages': [{'attributes': {'type': 'compile', 'flags': message['attributes']['flags']}, 'data': safe_source_file_name}]})
            publish(data=data)
    shutil.rmtree(folder_out_path)
    
    data = json.dumps({'messages': [{'attributes': {'type': 'link', 'flags': message['attributes']['flags']}, 'data': json.dumps(files)}]})
    publish(data=data)
    
    storage.delete_file(blob_name)
    return 'Ok', 200

def convert_sourcepath_to_objectpath(sourcepath):
    return sourcepath.rsplit(".", 1)[0] + ".o"

def compile_step(message):
    blob_name = message['data']
    
    messages.append(blob_name)
    source_file_path = '/tmp/' + blob_name
    with open(source_file_path, 'wb') as source_file:
        storage.download_file(blob_name, source_file)
        
    flags = json.loads(message['attributes']['flags'])
    
    object_file_path = convert_sourcepath_to_objectpath(source_file_path)
    msgs = compiler.compile(source_file_path, object_file_path, flags['compiler'], flags['compiler-flags'])
    os.remove(source_file_path)
    
    publish = queue.get_publisher('worker')
    with open(object_file_path, 'r') as object_file:
        object_file_name = object_file_path.rsplit('/',1)[-1]
        storage.upload_file(object_file, object_file_name)
        
    os.remove(object_file_path)
    storage.delete_file(blob_name)
    
    return 'Ok', 200
    
def link_step(message):
    
    messages.append(message['data'])
    files_attrs = json.loads(message['data'])
    flags = json.loads(message['attributes']['flags'])
    
    for file_attrs in files_attrs:
        if not storage.file_exists(file_attrs['blob_name']):
            data = json.dumps({'messages': [message]})
            publish(data=data)
            return 'Ok', 200
    
    rand = str(random.getrandbits(128))
    object_folder_path = '/tmp/' + rand + '-compiled/'
    os.makedirs(object_folder_path)
    for file_attrs in files_attrs:
        with open(object_folder_path + file_attrs['filename'], 'wb') as object_file:
            storage.download_file(file_attrs['blob_name'], object_file)
    
    object_paths = [object_folder_path + file_attrs['filename'] for file_attrs in files_attrs]
    executable_folder_path = '/tmp/' + rand + '-linked/' + flags['exename']
    linker.link(object_paths, executable_folder_path, flags['compiler'], flags['linker-flags'])
    shutil.rmtree(object_folder_path)
    
    with open(executable_folder_path, 'r') as executable_file:
        storage.upload_file(executable_file, flags['exename'])
    
    shutil.rmtree(executable_folder_path)
    
    return 'Ok', 200
    
    