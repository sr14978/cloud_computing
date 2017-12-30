
from google.cloud import storage
from werkzeug import secure_filename

client = storage.Client(project='cloudcomputingcompliler')
bucket = client.bucket('cloudcomputingcompilercode')

def upload_file(file):
  safe_filename = _safe_filename(file.filename)
  blob = bucket.blob(safe_filename)
  blob.upload_from_file(file)
  url = blob.public_url
  return url

deg _safe_filename():
  filename = secure_filename(filename)
  date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
  basename, extension = filename.rsplit('.', 1)
  return "{0}-{1}.{2}".format(basename, date, extension)