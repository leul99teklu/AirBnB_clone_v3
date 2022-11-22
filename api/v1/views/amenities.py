#!/usr/bin/python3
"""
HTTP requests for Amenity objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Gets all the amenity objects
    """
    amenities = storage.all('Amenity')
    json_amenities = []
    for amenity in amenities.values():
        json_amenities.append(amenity.to_json())
    return jsonify(json_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
    Get a specifc amenity object, by id
    """
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        return jsonify(amenity.to_json())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Delete amenity by id
    """
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        storage.delete(amenity)
        return (jsonify({}), 200)
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Create a new amenity
    """
    try:
        new_amenity_dict = request.get_json()
    except Exception:
        new_amenity_dict = None
    if not new_amenity_dict:
        abort(400, 'Not a JSON')
    if new_amenity_dict.get('name'):
        new_amenity = Amenity(new_amenity_dict)
        new_amenity.save()
        return (jsonify(new_amenity.to_json()), 201)
    else:
        abort(400, 'Missing name')


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Update a amenity
    """
    try:
        dict_update = request.get_json()
    except Exception:
        dict_update = None
    if not dict_update:
        abort(400, 'Not a JSON')
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        for key in dict_update.keys():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, dict_update[key])
        amenity.save()
        return (jsonify(amenity.to_json()), 200)
    abort(404)
