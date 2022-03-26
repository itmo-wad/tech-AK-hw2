from bson import json_util
from flask import render_template, session

from global_vars import app

@app.route('/profile')
def profile():
    #Get user data from session
    data = session['userdata']
    return render_template('profile.html', data=json_util.loads(data))