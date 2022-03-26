from bson import json_util
from flask import render_template, request, flash, url_for, redirect, session

from global_vars import app, mongo

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == "GET":
        return render_template('auth.html')
    else:
        email = request.form['email']
        passwd = request.form['pass']
        data = mongo.db.practice1.find_one({"email": email, "password": passwd})
        if data is None:
            flash('Wrong e-mail or password!', 'warning')
            return render_template('auth.html')
        else:
            # Session to store user data
            userdata = json_util.dumps(data)
            session['userdata'] = userdata

            return redirect(url_for('profile'))

