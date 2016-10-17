#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import datetime
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import JOIN, prefetch, fn

from utils import decorators
from database import Position, Bus, Assignment, OrderPosition

api = Blueprint('api', __name__)

# this method is for ease of use, defaults to current date
@api.route('/assignment', methods=['POST'])
@decorators.admin_required
def update_assignment():
    date = datetime.datetime.now().date()
    bus_name = request.form['bus_name']
    position_id = request.form['position_id']
    result = Assignment.create(
        date=date,
        bus=bus_name,
        position=position_id)
    return jsonify(success=True, result=model_to_dict(result)), 200


# this is for debug/special purposes, if you need to specify a date
@api.route('/assignment/<string:date>', methods=['POST'])
@decorators.admin_required
def update_assignment(date):
    bus_name = request.form['bus_name']
    position_id = request.form['position_id']
    result = Assignment.create(
        date=date,
        bus=bus_name,
        position=position_id)
    return jsonify(success=True, result=model_to_dict(result)), 200


# standard posting a new bus by order
@api.route('/assignment/by_order', methods=['POST'])
@decorators.admin_required
def update_assignment_by_order():
    date = datetime.datetime.now().date()
    bus_name = request.form['bus_name']
    order = Assignment.select(fn.COUNT(Assignment.id)).where(Assignment.date == date) + 1
    position = OrderPosition.get(OrderPosition.order == order).position
    result = Assignment.create(
        date=date,
        bus=bus_name,
        date_order=order,
        position=position)
    return jsonify(success=True, result=model_to_dict(result)), 200


# this is for special purposes, posting by order for a certain date
@api.route('/assignment/<string:date>/by_order', methods=['POST'])
@decorators.admin_required
def update_assignment_by_order(date):
    bus_name = request.form['bus_name']
    order = Assignment.select(fn.COUNT(Assignment.id)).where(Assignment.date == date) + 1
    position = OrderPosition.get(OrderPosition.order == order).position
    result = Assignment.create(
        date=date,
        bus=bus_name,
        date_order=order,
        position=position)
    return jsonify(success=True, result=model_to_dict(result)), 200


# list assignment objects
@api.route('/assignment', methods=['GET'])
def get_assignment_list():
    date = datetime.datetime.now().date()
    query = (Assignment.select(Assignment)
        .where(Assignment.date == date))
        #.join(Bus, JOIN.RIGHT_OUTER))
        #.join(Position, JOIN.RIGHT_OUTER)
    result = list(map(model_to_dict, query))
    return jsonify(success=True, result=result), 200


# list assignment objects for a specific date
@api.route('/assignment/<string:date>', methods=['GET'])
@decorators.admin_required # require admin if you request data from a different date
def get_assignment_list(date):
    query = (Assignment.select(Assignment)
        .where(Assignment.date == date))
        #.join(Bus, JOIN.RIGHT_OUTER))
        #.join(Position, JOIN.RIGHT_OUTER)
    result = list(map(model_to_dict, query))
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
