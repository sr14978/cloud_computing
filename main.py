from flask import Flask, redirect, render_template
import database
app = Flask(__name__)
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
 