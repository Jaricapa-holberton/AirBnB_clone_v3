#!/usr/bin/python3
"""State objects that handles all default RestFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, request, abort, make_response
from models.state import State
from models.city import City
from models.amenity import Amenity

app = Flask(__name__)


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """ Retrieves the list of all Amenity """
    amenitys = []
    for amenity in storage.all("Amenity").values():
        amenitys.append(amenity.to_dict())
    return jsonify(amenitys)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_by_id(amenity_id=None):
    """ Retrieves a Amenity by id """
    amenity_id = storage.get(Amenity, amenity_id)
    if amenity_id is None:
        abort(404)
    return jsonify(amenity_id.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities(amenity_id=None):
    """ Deletes a Amenity by id"""
    all_amenities = storage.all("Amenity").values()
    ame_del = []
    for ame in all_amenities:
        if ame.id == amenity_id:
            ame_del.append(ame.to_dict())
    if ame_del == []:
        abort(404)
    for ame in all_amenities:
        if ame.id == amenity_id:
            storage.delete(ame)
            storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenities():
    """function that create amenities"""
    data_to_post = request.get_json()
    if data_to_post is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    new_name = data_to_post.get('name')
    if new_name is None:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_amenity = Amenity(**data_to_post)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenities(amenity_id):
    """Fuction that update amenities"""
    amenity_to_mod = storage.get(Amenity, amenity_id)
    if amenity_to_mod is None:
        abort(404)
    data_to_mod = request.get_json()
    if data_to_mod is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in data_to_mod.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(amenity_to_mod, key, value)
    amenity_to_mod.save()
    return jsonify(amenity_to_mod.to_dict())
