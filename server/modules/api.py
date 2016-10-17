#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import datetime
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import JOIN, prefetch

from utils import decorators
from database import Position, Bus, Assignment

api = Blueprint('api', __name__)

@api.route('/assignment/<string:date>', methods=['POST'])
@decorators.admin_required
def update_assignment(date):
    bus_name = request.form['bus_name']
    position_id = request.form['position_id']
    result = Assignment.create(
        date=date,
        bus=bus_name,
        position=position_id,
        last_updated=datetime.datetime.now())
    return jsonify(success=True, result=model_to_dict(result)), 200


# list assignment objects
@api.route('/assignment/<string:date>', methods=['GET'])
def get_assignment_list(date):
    query = (Assignment.select(Assignment)
        .where(Assignment.date == date))
        #.join(Bus, JOIN.RIGHT_OUTER))
        #.join(Position, JOIN.RIGHT_OUTER)
    result = list(map(model_to_dict, query))
    return jsonify(success=True, result=result), 200


# list buses w/o an assignment
@api.route('/assignment/<string:date>/bus', methods=['GET'])
def get_assignments_bus(date):
    buses = Bus.select()
    assignments = Assignment.select().where(Assignment.date == date)
    buses_with_assignments = prefetch(buses, assignments)
    result = []
    for bus in buses_with_assignments:
        lst = bus.assignment_set_prefetch
        result.append(model_to_dict(lst[0]) if lst else dict(bus=model_to_dict(bus)))
    return jsonify(success=True, result=result), 200


# list positions w/o an assignment
@api.route('/assignment/<string:date>/position', methods=['GET'])
def get_assignments_position(date):
    positions = Position.select()
    assignments = Assignment.select().where(Assignment.date == date)
    positions_with_assignments = prefetch(positions, assignments)
    result = []
    for position in positions_with_assignments:
        lst = position.assignment_set_prefetch
        result.append(model_to_dict(lst[0]) if lst else dict(position=model_to_dict(position)))
    return jsonify(success=True, result=result), 200


@api.route('/bus', methods=['POST'])
@decorators.admin_required
def create_bus():
    bus_name = request.form['bus_name']
    try:
        result = Bus.create(name=bus_name)
        return jsonify(success=True, result=model_to_dict(result)), 200
    except peewee.IntegrityError:
        return jsonify(success=False, error="bus_name already exists"), 400


@api.route('/bus', methods=['GET'])
def get_bus_list():
    query = Bus.select()
    result = list(map(model_to_dict, query))
    return jsonify(success=True, result=result), 200


@api.route('/position', methods=['GET'])
def get_position_list():
    query = Position.select()
    result = list(map(model_to_dict, query))
    return jsonify(success=True, result=result), 200
