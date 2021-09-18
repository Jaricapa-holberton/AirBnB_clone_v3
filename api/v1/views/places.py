#!/usr/bin/python3
"""State view module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=["GET"],
                 strict_slashes=False)
def city_places(city_id=None):
    """retrieves a list of all places by city id"""
    my_city = storage.get(City, city_id)
    if my_city is None:
        abort(404)
    my_places = my_city.places
    my_places = [place.to_dict() for place in my_places]
    return (jsonify(my_places), 200)


@app_views.route('/places/place_id', methods=["GET"], strict_slashes=False)
def places(place_id):
    """ retrieve a place object"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    return (jsonify(my_place.to_dict()), 200)


@app_views.route('/places/<place_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place based on its id"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    storage.delete(my_place)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=["POST"],
                 strict_slashes=False)
def post_places(city_id):
    """ creates a place"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    my_city = storage.get(City, city_id)
    if my_city is None:
        abort(404)
    user_id = content.get("user_id")
    if user_id is None:
        abort(400, "Missing user_id")
    my_user = storage.get(User, user_id)
    if my_user is None:
        abort(404)
    name = content.get("name")
    if "name" is None():
        abort(400, "Missing name")
    new_place = Place()
    new_place.city_id = city_id

    for key, value in data.items():
        setattr(new_place, key, value)
    new_place.save()

    return (jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=["PUT"], strict_slashes=False)
def put_place(place_id):
    """ update a place by id"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(my_place, key, value)
    my_place.save()
    return (jsonify(my_place.to_dict()), 200)
