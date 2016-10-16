#!/usr/bin/env python3

import os
from flask import Flask, request, render_template

from utils import decorators
from database import db

app = Flask(__name__)
app.secret_key = 'blah'

# blueprints
from modules import api, admin
app.register_blueprint(api.api, url_prefix='/api')
app.register_blueprint(admin.admin, url_prefix='/admin')


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


# returns the image to be used - unsure if this is necessary, but if so, will standardize image
@app.route('/image', methods=['GET'])
def image():
    return app.send_static_file('image.png')


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000), host='0.0.0.0', debug=True)
