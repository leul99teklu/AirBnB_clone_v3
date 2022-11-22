#!/usr/bin/python3
"""
HTTP requests for City objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, State, City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    Grab cities from a specifc state
    """
    state = storage.get('State', state_id)
    if state:
        all_cities = state.cities
        json_cities = []
        for city in all_cities:
            json_cities.append(city.to_json())
        return jsonify(json_cities)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Get a specific city by id
    """
    city = storage.get('City', city_id)
    if city:
        return jsonify(city.to_json())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Delete a specific city by id
    """
    city = storage.get('City', city_id)
    if city:
        storage.delete(city)
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Create a city connected to a state
    """
    state = storage.get('State', state_id)
    if state:
        try:
            city_dict = request.get_json()
        except Exception:
            city_dict = None
        if city_dict is None:
            abort(400, 'Not a JSON')
        if city_dict.get('name') is None:
            abort(400, 'Missing name')
        city_dict['state_id'] = state_id
        city = City(city_dict)
        city.save()
        return jsonify(city.to_json()), 201
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """
    Update a city by city id
    """
    city = storage.get('City', city_id)
    if city:
        try:
            update_dict = request.get_json()
        except Exception:
            update_dict = None
        if update_dict is None:
            abort(400, 'Not a JSON')
        for key in update_dict.keys():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, update_dict[key])
        city.save()
        return jsonify(city.to_json()), 200
    abort(404)
