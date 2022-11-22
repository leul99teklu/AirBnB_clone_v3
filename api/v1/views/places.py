#!/usr/bin/python3
"""
HTTP requests for Place objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
    Grab all places in a specific city
    """
    city = storage.get('City', city_id)
    if city:
        all_places = storage.all('Place')
        city_places = []
        for place in all_places.values():
            if place.city_id == city_id:
                city_places.append(place.to_json())
        return jsonify(city_places)
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """
    Grab a specific place by id
    """
    place = storage.get('Place', place_id)
    if place:
        return jsonify(place.to_json())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Delete a place object by id
    """
    place = storage.get('Place', place_id)
    if place:
        storage.delete(place)
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Create a new place connected to a city
    """
    city = storage.get('City', city_id)
    if city:
        try:
            place_dict = request.get_json()
        except Exception:
            place_dict = None
        if place_dict is None:
            abort(400, 'Not a JSON')
        if place_dict.get('user_id') is None:
            abort(400, 'Missing user_id')
        if place_dict.get('name') is None:
            abort(400, 'Missing name')
        if storage.get('User', place_dict.get('user_id')) is None:
            abort(404)
        place_dict['city_id'] = city_id
        new_place = Place(place_dict)
        new_place.save()
        return jsonify(new_place.to_json()), 201
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    Update the place specified by given id
    """
    place = storage.get('Place', place_id)
    if place:
        try:
            update_dict = request.get_json()
        except Exception:
            update_dict = None
        if update_dict is None:
            abort(400, 'Not a JSON')
        for key in update_dict.keys():
            if key not in ['id', 'user_id', 'city_id', 'created_at',
                           'updated_at']:
                setattr(place, key, update_dict[key])
        place.save()
        return jsonify(place.to_json()), 200
    abort(404)
