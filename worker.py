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
import preprocessor
import compiler
import linker
from google.api_core.exceptions import InvalidArgument

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
    print("unzip_step: " + json.dumps(message))
    blob_name = message['data']
    flags = json.loads(message['attributes']['flags'])
    
    messages.append(blob_name)
    rand = str(random.getrandbits(128))
    zip_filepath = '/tmp/source-' + rand + '.zip'
    with open(zip_filepath, 'wb') as zip_file:
        storage.download_file(blob_name, zip_file)
        
    unzipped_folder_path = '/tmp/' + rand + '-unpacked'
    sources = unzipper.unzip(zip_filepath, unzipped_folder_path)  
    os.remove(zip_filepath)
    
    try:
        publish = queue.get_publisher('worker')
    except InvalidArgument:
        return "Task queue not initialised", 200
    
    files_attributes = []
    preprocessed_folder_path = '/tmp/' + rand + '-preprocessed'
    os.makedirs(preprocessed_folder_path)
    for source_file_name in sources:
        print("dealing with: " + source_file_name)
        if source_file_name.endswith('.c') or source_file_name.endswith('.cpp'):
            success, msg = preprocessor.preprocess(
                unzipped_folder_path + '/' + source_file_name,
                preprocessed_folder_path + '/' + source_file_name,
                flags['compiler'], flags['compiler-flags']
            )
            
            safe_source_file_name = storage.safe_filename(source_file_name)
            file_attributes = {
                                'object_filename': convert_sourcepath_to_objectpath(source_file_name),
                                'object_blobname': convert_sourcepath_to_objectpath(safe_source_file_name),
                                'msg_blobname': convert_sourcepath_to_msg_path(safe_source_file_name)
                              }
            files_attributes.append(file_attributes)
            
            if success:
                print("Preprocessed: " + source_file_name)
                with open(preprocessed_folder_path + '/' + source_file_name, 'r') as source_file:
                    
                    storage.upload_file(source_file, safe_source_file_name)
                    print("Uploaded file: " + source_file_name + " to: " + safe_source_file_name)
                    
                    data = json.dumps({
                      'messages': [{
                        'attributes': {
                          'type': 'compile',
                          'flags': message['attributes']['flags'],
                          'file_attributes': file_attributes
                        },
                        'data': safe_source_file_name
                      }]
                    })
                    publish(data=data)
            else:
                print("Preprocessed of " + source_file_name + " failed: " + ','.join(msg))
                storage.upload_string(msg, file_attributes['msg_blobname'])
            
    shutil.rmtree(preprocessed_folder_path)
    shutil.rmtree(unzipped_folder_path)
    
    data = json.dumps({'messages': [{'attributes': {
      'type': 'link',
      'flags': message['attributes']['flags'],
      'job_result_blobname': message['attributes']['job_result_blobname'],
      'executable_blobname': message['attributes']['executable_blobname']
    }, 'data': json.dumps(files_attributes)}]})
    print("Submitting link job: " + data)
    publish(data=data)
    
    storage.delete_file(blob_name)
    return 'Ok', 200

def convert_sourcepath_to_objectpath(sourcepath):
    return sourcepath.rsplit(".", 1)[0] + ".o"

def convert_sourcepath_to_msg_path(sourcepath):
    return sourcepath.rsplit(".", 1)[0] + ".msg"

def compile_step(message):
    print("compile_step: " + json.dumps(message))
    source_blob_name = message['data']
    
    messages.append(source_blob_name)
    rand = str(random.getrandbits(128))
    working_folder = '/tmp/source-' + rand + '/'
    os.makedirs(working_folder)
    source_file_path = working_folder + source_blob_name
    
    if storage.file_exists(message['attributes']['file_attributes']['msg_blobname']):
        shutil.rmtree(working_folder)
        return "Ok", 200
    
    with open(source_file_path, 'wb') as source_file:
        storage.download_file(source_blob_name, source_file)
        print("Downloaded sourcefile: " + source_file_path)
        
    flags = json.loads(message['attributes']['flags'])
    
    object_file_path = working_folder + message['attributes']['file_attributes']['object_filename']
    success, msg = compiler.compile(source_file_path, object_file_path, flags['compiler'], flags['compiler-flags'])
    os.remove(source_file_path)
    
    msg_blobname = message['attributes']['file_attributes']['msg_blobname']
    storage.upload_string(msg, msg_blobname)
    print("Storing msg: " + msg + " to blobname: " + msg_blobname)
    
    if success:
      with open(object_file_path, 'r') as object_file:
          storage.upload_file(object_file, message['attributes']['file_attributes']['object_blobname'])
        
    shutil.rmtree(working_folder)
    storage.delete_file(source_blob_name)
    
    return 'Ok', 200
    
def link_step(message):
    print("link_step: " + json.dumps(message))
    messages.append(message['data'])
    attrs_files = json.loads(message['data'])
    flags = json.loads(message['attributes']['flags'])
    
    for attrs_file in attrs_files:
        if not storage.file_exists(attrs_file['msg_blobname']):
            print("Could not find: " + attrs_file['msg_blobname'] + " so rescheduling and exiting")
            data = json.dumps({'messages': [message]})
            try:
                publish = queue.get_publisher('worker')
            except InvalidArgument:
                return "Task queue not initialised", 200
            publish(data=data)
            return 'Ok', 200
    
    rand = str(random.getrandbits(128))
    object_folder_path = '/tmp/' + rand + '-compiled/'
    os.makedirs(object_folder_path)
    
    def download_object_files():
        object_filenames = [attrs_file['object_filename'] for attrs_file in attrs_files]
        print("Downloading object files for linking: " + ','.join(object_filenames))
        for attrs_file in attrs_files:
            with open(object_folder_path + attrs_file['object_filename'], 'wb') as object_file:
                storage.download_file(attrs_file['object_blobname'], object_file)
        return [object_folder_path + attrs_file['object_filename'] for attrs_file in attrs_files]
    
    msgs = [storage.download_string(attrs_file['msg_blobname']) for attrs_file in attrs_files]
    print("Downloaded all compiler messages: " + ','.join(msgs))
    
    executable_folder_path = '/tmp/' + rand + '-linked/'
    os.makedirs(executable_folder_path)
    executable_path = executable_folder_path + flags['exename']
    
    msg = linker.link(msgs, download_object_files, executable_path, flags['compiler'], flags['linker-flags'])
    shutil.rmtree(object_folder_path)
    
    ret = {
      'success': isinstance(msg, linker.Success),
      'messages': msg.msgs,
      'executable_name': flags['exename']
    }
    
    print("Linker returned: " + json.dumps(ret))
    
    storage.upload_string(json.dumps(ret), message['attributes']['job_result_blobname'])
    
    if isinstance(msg, linker.Success):
        with open(executable_path, 'r') as executable_file:
            storage.upload_file(executable_file, message['attributes']['executable_blobname'])
            print("Uploaded executable file: " + message['attributes']['executable_blobname'])
       
    shutil.rmtree(executable_folder_path)
    
    for attrs_file in attrs_files:
        if storage.file_exists(attrs_file['object_blobname']):
            storage.delete_file(attrs_file['object_blobname'])
        storage.delete_file(attrs_file['msg_blobname'])
        print("Deleting object blob: " + attrs_file['object_blobname'] + " and msg blob: " + attrs_file['msg_blobname'])
    
    return 'Ok', 200
    
    