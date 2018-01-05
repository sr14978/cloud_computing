from flask import Flask, redirect, render_template, session
import database
from oauth2client.contrib.flask_util import UserOAuth2
import httplib2
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = '\xde{\xcb\xd0\x97gi\x9a\x9f\x18G\xb2\x18\xed8d\xd2\x9e[\xa4=\xf5\xac\xa4'

def _request_user_info(credentials):
    http = httplib2.Http()
    credentials.authorize(http)
    resp, content = http.request(
        'https://www.googleapis.com/plus/v1/people/me')

    if resp.status != 200:
        print("Error while obtaining user profile: \n%s: %s", resp, content)
        return
        
    google_user = json.loads(content.decode('utf-8'))
    user_id = google_user['id']
    session['user_id'] = user_id
    
    user = database.get_user(user_id)
    if user == None:
        database.create_user({'user_id': user_id, 'name': google_user['displayName']})
    
    print("credentials: ", json.loads(content.decode('utf-8')))

oauth2 = UserOAuth2()
oauth2.init_app(
        app,
        scopes=['email', 'profile'],
        authorize_callback=_request_user_info,
        client_id='540065309258-l47khtteovcjo07i65gbhp85tf83uqec.apps.googleusercontent.com',
        client_secret='Uzka-as21BkyzH53OeYnfniW')

@app.route("/")
@oauth2.required
def index():
    return redirect('/static/index.html')
    
@app.route("/history/index.html")
@oauth2.required
def history():
    user_id = session['user_id']
    user = database.get_user(user_id)
    if user != None:
        return render_template('history.html', executables=user['executables'])
    else:
        return "Invalid user", 401

@app.route("/test")
@oauth2.required
def test():
    return "Test oauth2: " + session['user_id'], 200
 