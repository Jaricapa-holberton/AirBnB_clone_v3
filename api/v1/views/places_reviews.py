#!/usr/bin/python3
"""Review module"""
from flask import Flask, jsonify, request, abort, make_response
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """get information for all reviews"""
    place_to_rew = storage.get(Place, place_id)
    if place_to_rew is None:
        abort(404)
    reviews = []
    for review in place_to_rew.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review_by_id(review_id):
    """get information for the specified review"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """delete review by id"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review_create(place_id):
    """create a new review"""
    data_to_post = request.get_json()
    if data_to_post is None:
        return "Not a JSON", 400
    place_to_rew = storage.get(Place, place_id)
    if not place_to_rew:
        abort(404)
    if data_to_post.get('user_id') is None:
        return "Missing user_id", 400
    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)
    if data_to_post.get('text') is None:
        return "Missing text", 400
    else:
        review = Review(**data_to_post)
        review.place_id = place_id
        review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """update a review"""
    if request.get_json() is None:
        return "Not a JSON", 400
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    ignored = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for attr, val in request.get_json().items():
        if attr not in ignored:
            setattr(review, attr, val)
    review.save()
    return jsonify(review.to_dict()), 200
