# flask server to create rest api

import os
import datetime

from flask import Flask, request, jsonify
from playhouse.shortcuts import model_to_dict, dict_to_model

from database import Position, Bus, Assignment, db


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return app.send_static_file('index.html')

@app.route('/test', methods=['GET']) #testing page
def test():
    return app.send_static_file('test.html')

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


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000), host='0.0.0.0', debug=True)

