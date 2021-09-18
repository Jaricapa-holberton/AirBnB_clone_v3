#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul AP"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=["GET"], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def state(state_id=None):
    """retrieves a list of all states or state by id"""
    if state_id is None:
        states = storage.all("State")
        my_states = [value.to_dict() for key, value in states.items()]
        return jsonify(my_states)

    my_states = storage.get(State, state_id)
    if my_states is None:
        abort(404)
    return jsonify(my_states.to_dict())


@app_views.route('/states/<state_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_states(state_id):
    """Deletes a state based on its id"""
    my_state = storage.get(State, state_id)
    if my_state is None:
        abort(404)
    storage.delete(my_state)
    storage.save()
    return (jsonify({}))


@app_views.route('/states', methods=["POST"], strict_slashes=False)
def post_states():
    """ creates a state"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data.keys():
        abort(400, "Missing name")
    new_data = State(**data)
    new_data.save()

    return (jsonify(new_data.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=["PUT"], strict_slashes=False)
def put_states(state_id):
    """ update a state"""
    my_state = storage.get(State, state_id)
    if my_state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(my_state, key, value)
    my_state.save()
    return (jsonify(my_state.to_dict()), 200)
