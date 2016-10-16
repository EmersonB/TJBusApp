#!/usr/bin/env python3

import datetime
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict, dict_to_model

from utils import decorators
from database import Position, Bus, Assignment

api = Blueprint('api', __name__)

@api.route('/assignment/<string:date>/<string:bus_name>', methods=['POST'])
@decorators.admin_required
def update_assignment(date, bus_name):
    position_id = request.form['position_id']
    obj = Assignment.create(
        date=date,
        bus=bus_name,
        position=position_id,
        last_updated=datetime.datetime.now())
    return jsonify(success=True, result=model_to_dict(obj)), 200


@api.route('/assignment/<string:date>/<string:bus_name>', methods=['GET'])
def get_assignment(date, bus_name):
    try:
        result = Assignment.get(Assignment.bus == bus_name, Assignment.date == date)
        return jsonify(success=True, result=model_to_dict(result)), 200
    except Assignment.DoesNotExist as e:
        return jsonify(success=False, error='Assignment does not exist'), 404


# get all bus assignments
@api.route('/assignment/<string:date>', methods=['GET'])
def get_assignment_list(date):
    query = Assignment.select().where(Assignment.date == date)
    result = list(map(model_to_dict, query))
    return jsonify(success=True, result=result), 200


@api.route('/bus', methods=['POST'])
@decorators.admin_required
def create_bus():
    bus_name = request.form['bus_name']
    Bus.create(name=bus_name)
    return jsonify(success=True), 200


@api.route('/bus', methods=['GET'])
def list_buses():
    query = Bus.select()
    result = list(map(model_to_dict, query))
    return jsonify(success=True, result=result), 200
