#!/usr/bin/python3
"""
HTTP requests for User objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Gets all the user objects
    """
    users = storage.all('User')
    json_users = []
    for user in users.values():
        json_users.append(user.to_json())
    return jsonify(json_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Get a specifc user object, by id
    """
    user = storage.get('User', user_id)
    if user:
        return jsonify(user.to_json())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Delete user by id
    """
    user = storage.get('User', user_id)
    if user:
        storage.delete(user)
        return (jsonify({}), 200)
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Create a new user
    """
    try:
        new_user_dict = request.get_json()
    except Exception:
        new_user_dict = None
    if not new_user_dict:
        abort(400, 'Not a JSON')
    if new_user_dict.get('email'):
        if new_user_dict.get('password'):
            new_user = User(new_user_dict)
            new_user.save()
            return (jsonify(new_user.to_json()), 201)
        else:
            abort(400, 'Missing password')
    else:
        abort(400, 'Missing email')


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Update a user
    """
    try:
        dict_update = request.get_json()
    except Exception:
        dict_update = None
    if not dict_update:
        abort(400, 'Not a JSON')
    user = storage.get('User', user_id)
    if user:
        for key in dict_update.keys():
            if key not in ['id', 'created_at', 'updated_at', 'email']:
                setattr(user, key, dict_update[key])
        user.save()
        return (jsonify(user.to_json()), 200)
    abort(404)
