import datetime
from google.cloud import storage
from werkzeug import secure_filename

client = storage.Client(project='cloudcomputingcompiler')
bucket = client.bucket('cloudcomputingcompilercodecontainer')

def upload_file(file, safe_filename):
    blob = bucket.blob(safe_filename)
    blob.upload_from_file(file)
    url = blob.public_url
    return url
    
def upload_string(string, safe_filename):
    blob = bucket.blob(safe_filename)
    blob.upload_from_string(string)
    url = blob.public_url
    return url

def download_file(filename, file):
    blob = bucket.blob(filename)
    blob.download_to_file(file)
  
def download_string(filename):
    blob = bucket.blob(filename)
    return blob.download_as_string()
  
def delete_file(filename):
    blob = bucket.blob(filename)
    blob.delete()
 
def file_exists(filename):
  blob = bucket.blob(filename)
  return blob.exists()
 
def safe_filename(filename):
  filename = secure_filename(filename)
  date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
  basename, extension = filename.rsplit('.', 1)
  return "{0}-{1}.{2}".format(basename, date, extension)