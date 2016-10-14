# flask server to create rest api

import os
from flask import Flask, request, jsonify
from playhouse.shortcuts import model_to_dict, dict_to_model

from database import Position, Bus, Assignment, db


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return app.send_static_file('index.html')


# returns the image to be used - unsure if this is necessary, but if so, will standardize image
@app.route('/image', methods=['GET'])
def image():
    return app.send_static_file('image.png')


@app.route('/assignment/<string:bus_name>', methods=['GET', 'POST'])
def update_assignment(bus_name=None):
    if not bus_name:
        return {'error': 'Please specify a bus_name.'}, 400

    if request.method == 'POST':
        # TODO: check authentication here
        date = request.form['date']
        position_id = request.form['position_id']

        obj = Assignment(
            date=date,
            name=bus_name,
            position=position_id,
            last_updated=datetime.datetime.now())
        obj.save()

        return jsonify(success=True), 200

    else:
        # TODO also auth here - security concern
        date = request.form['date']  # TODO: fix

        result = Assignment.get(Assignment.bus == bus_id and Assignment.date == date)
        if result is None:
            return {'error': 'bus_id does not exist'}, 404
        else:
            return jsonify(success=True, result=model_to_dict(result)), 200


# get all bus assignments
@app.route('/assignment', methods=['GET'])
def get_assignment_list():
    # TODO auth here
    date = request.form['date']

    query = Assignment.select().where(Assignment.date == date)
    result = list(map(model_to_dict, query))
    return jsonify(success=True, result=result), 200


@app.route('/bus', methods=['GET', 'POST'])
def get_bus_list():
    if request.method == 'POST':
        bus_name = request.form['bus_name']
        obj = Bus(name=bus_name)
        obj.save()
        return jsonify(success=True), 200
            
    else:
        query = Bus.select()
        print(query)
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

