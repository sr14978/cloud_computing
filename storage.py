import datetime
from google.cloud import storage
from werkzeug import secure_filename

client = storage.Client(project='cloudcomputingcompliler')
bucket = client.bucket('cloudcomputingcompilercode')

def upload_file(file, safe_filename):
    blob = bucket.blob(safe_filename)
    blob.upload_from_file(file)
    url = blob.public_url
    return url

def download_file(filename, file):
    blob = bucket.blob(filename)
    blob.download_to_file(file)
  
def delete_file(filename):
    blob = bucket.blob(filename)
    blob.delete()
 
def file_exists(filename):
  return bucket.exists(filename)
 
def safe_filename(filename):
  filename = secure_filename(filename)
  date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
  basename, extension = filename.rsplit('.', 1)
  return "{0}-{1}.{2}".format(basename, date, extension)