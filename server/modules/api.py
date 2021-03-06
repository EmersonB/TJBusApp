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
    return update_assignment_with_date(datetime.datetime.now().date())

# this is for debug/special purposes, if you need to specify a date
@api.route('/assignment/<string:date>', methods=['POST'])
@decorators.admin_required
def update_assignment_with_date(date):
    bus_name = request.form['bus_name']
    position_id = request.form['position_id']
    try:
        result = Assignment.create(
            date=date,
            bus=bus_name,
            position=position_id)
        return jsonify(success=True, result=model_to_dict(result)), 200
    except peewee.IntegrityError: # need bus_name + date pair to be unique
        return jsonify(success=False, error="bus_name + date pair not unique"), 400


# standard posting a new bus by order
@api.route('/assignment/by_order', methods=['POST'])
@decorators.admin_required
def update_assignment_by_order():
    return update_assignment_by_order_with_date(datetime.datetime.now().date())


# this is for special purposes, posting by order for a certain date
@api.route('/assignment/<string:date>/by_order', methods=['POST'])
@decorators.admin_required
def update_assignment_by_order_with_date(date):
    bus_name = request.form['bus_name']
    order = Assignment.select(fn.COUNT(Assignment.id)).where(Assignment.date == date) + 1
    position = OrderPosition.get(OrderPosition.order == order).position
    try:
        result = Assignment.create(
            date=date,
            bus=bus_name,
            date_order=order,
            position=position)
        return jsonify(success=True, result=model_to_dict(result)), 200
    except peewee.IntegrityError: # need bus_name + date pair to be unique
        return jsonify(success=False, error="bus_name + date pair not unique"), 400


#####################################################################################

# this block is very sketchy at the moment

# TODO: if bus location (mapped to arrival order) already exists
# 1. set new bus's position to position of that order
# 2. bump rest of buses
# also check if there are empty slots? this is a mess

# allow admin to specify order position
@api.route('/assignment/by_position', methods=['POST'])
@decorators.admin_required
def update_assignment_by_order():
    return update_assignment_by_order_with_date(datetime.datetime.now().date())


# for specific date
@api.route('/assignment/<string:date>/by_position', methods=['POST'])
@decorators.admin_required
def update_assignment_by_order_with_date(date):
    bus_name = request.form['bus_name']
    order = request.form['order']
    position = OrderPosition.get(OrderPosition.order == order).position
    try:
        result = Assignment.create(
            date=date,
            bus=bus_name,
            date_order=order,
            position=position)
        return jsonify(success=True, result=model_to_dict(result)), 200
    except peewee.IntegrityError: # need bus_name + date pair to be unique
        return jsonify(success=False, error="bus_name + date pair not unique"), 400

#####################################################################################


# list assignment objects
@api.route('/assignment', methods=['GET'])
def get_assignment_list():
    return get_assignment_list_with_date(datetime.datetime.now().date())


# list assignment objects for a specific date
@api.route('/assignment/<string:date>', methods=['GET'])
@decorators.admin_required # require admin if you request data from a different date
def get_assignment_list_with_date(date):
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
