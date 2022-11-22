#!/usr/bin/python3
"""
HTTP requests for Review objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """
    Get all reviews for a place, by place id
    """
    place = storage.get('Place', place_id)
    if place:
        all_reviews = storage.all('Review')
        place_reviews = []
        for review in all_reviews.values():
            if review.place_id == place_id:
                place_reviews.append(review.to_json())
        return jsonify(place_reviews)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """
    Get specific review by id
    """
    review = storage.get('Review', review_id)
    if review:
        return jsonify(review.to_json())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Delete a review specified by id
    """
    review = storage.get('Review', review_id)
    if review:
        storage.delete(review)
        return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Create a review connected to a place
    """
    place = storage.get('Place', place_id)
    if place:
        try:
            review_dict = requst.get_json()
        except Exception:
            review_dict = None
        if review_dict is None:
            abort(400, 'Not a JSON')
        if review_dict.get('user_id') is None:
            abort(400, 'Missing user_id')
        if storage.get('User', review_dict['user_id']) is None:
            abort(404)
        if review_dict.get('text') is None:
            abort(400, 'Missing text')
        review_dict['place_id'] = place_id
        new_review = Review(review_dict)
        new_review.save()
        return jsonify(new_review.to_json()), 201
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Update the review specified by id
    """
    review = storage.get('Review', review_id)
    if review:
        try:
            update_dict = request.get_json()
        except Exception:
            update_dict = None
        if update_dict is None:
            abort(400, 'Not a JSON')
        for key in update_dict.keys():
            if key not in ['id', 'user_id', 'place_id', 'created_at',
                           'updated_at']:
                setattr(review, key, update_dict[key])
        review.save()
        return jsonify(review.to_json()), 200
    abort(404)
