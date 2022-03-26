import datetime
import os
import random

from flask import render_template, request, flash, url_for, redirect
from werkzeug.utils import secure_filename

import config
from global_vars import app, mongo

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    else:
        name = request.form['name']
        passwd = request.form['pass']
        github = request.form['github']
        university = request.form['university']
        email = request.form['email']

        if 'fileID' not in request.files:
            flash('No file provided', 'danger')
            return render_template('signup.html')

        file = request.files['fileID']

        # An if actually works by computing a value for the logical expression you give it: True or False. If you simply use a variable name (or a literal string like "hello") instead of a logical test, the rule is: An empty string counts as False, all other strings count as True. Empty lists and the number zero also count as false, and most other things count as true.
        # Check if all fields are filled
        if not (name and passwd and name and github and university and email):
            flash('Please fill in all fields', 'warning')
            return render_template('signup.html')

        # Check if name is already registered
        if mongo.db.practice1.find_one({"email": email}): #true, if there was one entry found in database
            flash('This name is already registered. Do you want to go to the <a href="' + url_for("auth") + '">authentication page</a>?', 'warning')
            return render_template('signup.html')

        # Check if with image file is everything okay and process image file
        filename = handleImageUpload(file)
        if not filename:
            # there was an error, reload page to show flask message
            return render_template('signup.html')

        # Fall-through, if no if condition above is met, we can add the entry.
            # TODO: For more security, we could generate here a hash of the password via generate_password_hash() and
            #  check_password_hash()
        mongo.db.practice1.insert_one({"email": email, "password": passwd, "pic_file_name": filename, "fullname": name, "github": github, "github_url": config.GITHUB_PROFILE_PAGE_URL + github, "university": university, "creation_date": datetime.date.today().strftime('%d.%m.%Y')})

        # Check if inserting has worked
        if mongo.db.practice1.find_one({"email": email, "password": passwd}):
            #adding new name to database has worked
            flash('Successfully registered! Please log in with your new access credentials', 'success')
            return redirect(url_for('auth'))
        else:
            flash('Something went wrong. Try again', 'warning')
            return render_template('signup.html')

def is_file_allowed(filename):
    return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS)

def handleImageUpload(file):
    """Checks if the image is not malicious and if not, saves the image. Returns the new filename or, in case of errors, an empty string."""
    if file.filename == '':
        flash('No file selected', 'danger')
        return ""

    if not is_file_allowed(file.filename):
        flash('Invalid file extension', 'danger')
        return ""

    if file:
        filename = secure_filename(file.filename)
        # Set random filename, otherwise user could overwrite each other
        filename = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S') + '_' + str(random.randint(100, 999)) + '_' + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename

    return ""