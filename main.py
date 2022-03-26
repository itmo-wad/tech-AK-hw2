from flask import Flask, redirect, url_for
from flask_pymongo import PyMongo

import global_vars, config

app = Flask(__name__)
app.config["MONGO_URI"] = config.MONGO_URI
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
mongo = PyMongo(app)

global_vars.init(app_ref=app, mongo_ref=mongo)
import sites.auth, sites.signup, sites.profile

@app.route('/')
def main():
    return redirect(url_for('auth'))


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)