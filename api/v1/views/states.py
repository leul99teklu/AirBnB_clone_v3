#!/usr/bin/python3
"""
HTTP requests for State objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Gets all the state objects
    """
    states = storage.all('State')
    json_states = []
    for state in states.values():
        json_states.append(state.to_json())
    return jsonify(json_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Get a specifc state object, by id
    """
    state = storage.get('State', state_id)
    if state:
        return jsonify(state.to_json())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Delete state by id
    """
    state = storage.get('State', state_id)
    if state:
        storage.delete(state)
        return (jsonify({}), 200)
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Create a new state
    """
    try:
        new_state_dict = request.get_json()
    except Exception:
        new_state_dict = None
    if not new_state_dict:
        abort(400, 'Not a JSON')
    if new_state_dict.get('name'):
        new_state = State(new_state_dict)
        new_state.save()
        return (jsonify(new_state.to_json()), 201)
    else:
        abort(400, 'Missing name')


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Update a state
    """
    try:
        dict_update = request.get_json()
    except Exception:
        dict_update = None
    if not dict_update:
        abort(400, 'Not a JSON')
    state = storage.get('State', state_id)
    if state:
        for key in dict_update.keys():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, dict_update[key])
        state.save()
        return (jsonify(state.to_json()), 200)
    abort(404)
