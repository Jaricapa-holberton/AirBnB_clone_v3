#!/user/bin/python3
"""User module"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, request, abort, make_response
from models.state import State
from models.city import City
from models.user import User

app = Flask(__name__)


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def all_users():
    """ Retrieves the list of all Users """
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def user_by_id(user_id):
    """ Retrieves a User by id """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """ Delete user by id """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """create a new user"""
    data_to_post = request.get_json()
    if data_to_post is None:
        return "Not a JSON", 400
    if data_to_post.get('email') is None:
        return "Missing email", 400
    if data_to_post.get('password') is None:
        return "Missing password", 400
    else:
        user = User(**data_to_post)
        user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """ Update a user """
    user_to_mod = storage.get(User, user_id)
    if user_to_mod is None:
        abort(404)
    data_to_mod = request.get_json()
    if data_to_mod is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in data_to_mod.items():
        if key in ['id', 'email', 'created_at', 'updated_at']:
            continue
        else:
            setattr(user_to_mod, key, value)
    user_to_mod.save()
    return jsonify(user_to_mod.to_dict()), 200
