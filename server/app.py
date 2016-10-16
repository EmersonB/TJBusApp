# flask server to create rest api

import os
import datetime
from flask import Flask, request, render_template, jsonify, session, flash, redirect, url_for
from playhouse.shortcuts import model_to_dict, dict_to_model

from utils import pwhash, decorators
from database import db, Position, Bus, Assignment, AdminUser


app = Flask(__name__)
app.secret_key = 'blah'


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


# returns the image to be used - unsure if this is necessary, but if so, will standardize image
@app.route('/image', methods=['GET'])
def image():
    return app.send_static_file('image.png')


@app.route('/assignment/<string:date>/<string:bus_id>', methods=['GET', 'POST'])
def update_assignment(date, bus_id=None):
    if not bus_id:
        return jsonify(success=False, error='Please specify a bus_id.'), 400

    if request.method == 'POST':
        # TODO: check authentication here
        position_id = request.form['position_id']

        obj = Assignment(
            date=date,
            bus=bus_id,
            position=position_id,
            last_updated=datetime.datetime.now())
        obj.save()

        return jsonify(success=True), 200

    else:
        result = Assignment.get(Assignment.bus == bus_id and Assignment.date == date)
        if result is None:
            return jsonify(success=False, error='bus_id does not exist'), 404
        else:
            return jsonify(success=True, result=model_to_dict(result)), 200


# get all bus assignments
@app.route('/assignment/<string:date>', methods=['GET'])
def get_assignment_list(date):
    query = Assignment.select().where(Assignment.date == date)
    result = list(map(model_to_dict, query))
    return jsonify(success=True, result=result), 200


@app.route('/bus', methods=['GET', 'POST'])
def get_bus_list():
    if request.method == 'POST':
        # TODO check auth!!!
        bus_name = request.form['bus_name']
        obj = Bus(name=bus_name)
        obj.save()
        return jsonify(success=True), 200

    else:
        query = Bus.select()
        result = list(map(model_to_dict, query))
        return jsonify(success=True, result=result), 200


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = AdminUser.get(AdminUser.username == username)
            if pwhash.verify(password, user.password):
                session['admin'] = username
                return redirect(url_for('.admin_home'))
        except AdminUser.DoesNotExist:
            pass

        flash('Username/password are incorrect.')
        return render_template('admin/login.html')

    else:
        if 'admin' in session and session['admin']:
            flash('Warning: you are already logged in as {}'.format(session['admin']))
        return render_template('admin/login.html')


@app.route('/admin/logout', methods=['GET'])
@decorators.admin_required
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('.admin_login'))


@app.route('/admin/', methods=['GET'])
@decorators.admin_required
def admin_home():
    return render_template('admin/index.html')


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000), host='0.0.0.0', debug=True)
