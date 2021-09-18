#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul AP"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, state, city
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=["GET"],
                 strict_slashes=False)
def city(state_id=None):
    """retrieves a list of all cities by state id"""
    my_states = storage.get(State, state_id)
    if my_states is None:
        abort(404)
    cities = my_states.cities
    my_cities = [city.to_dict() for city in cities]
    return (jsonify(my_cities), 200)


@app_views.route('/cities/<city_id>', methods=["GET"], strict_slashes=False)
def city_by_id(city_id=None):
    """retrieve a city by id"""
    my_city = storage.get(City, city_id)
    if my_city is None:
        abort(404)
    return (jsonify(my_city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """delete a city by id"""
    my_city = storage.get(City, city_id)
    if my_city is None:
        abort(404)
    storage.delete(my_city)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def post_city(state_id):
    """create a city in a state"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    name = data.get("name")
    if "name" not in data:
        abort(400, "Missing name")
    my_state = storage.get(State, state_id)
    if my_state is None:
        abort(404)
    new_city = City()
    new_city.state_id = id
    new_city.name = name
    new_city.save()

    return (jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    """ update a state"""
    my_city = storage.get(City, city_id)
    if my_city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(my_city, key, value)

    my_city.save()
    return (jsonify(my_city.to_dict()), 200)
