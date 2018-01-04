from flask import Flask, redirect, render_template
import database
from oauth2client.contrib.flask_util import UserOAuth2

oauth2 = UserOAuth2()

app = Flask(__name__)

def _request_user_info(creds):
    print("credentials: " + str(creds))


oauth2.init_app(
        app,
        scopes=['email', 'profile'],
        authorize_callback=_request_user_info,
        client_id='540065309258-l47khtteovcjo07i65gbhp85tf83uqec.apps.googleusercontent.com',
        client_secret='Uzka-as21BkyzH53OeYnfniW')

@app.route("/")
def index():
    return redirect('/static/index.html')
    
@app.route("/history/<user_id>")
def history(user_id):
    user = database.get_user(user_id)
    if user != None:
        return render_template('history.html', executables=user['executables'])
    else:
        return "Invalid user", 401

@app.route("/test")
@oauth2.required
def test():
    return "Test oauth2", 200
 