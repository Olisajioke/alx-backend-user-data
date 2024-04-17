#!/usr/bin/env python3
"""A module that handles all views for the User class.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """GET /api/v1/users
    Return:
      - multiple User objects JSON represented.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """GET /api/v1/users/:id
    Path parameter:
      - User ID.
    Return:
      - one User object JSON represented.
      - error 404 if the User ID doesn't exist.
    """
    if user_id is None:
        abort(404)
    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        else:
            return jsonify(request.current_user.to_json())
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """DELETE /api/v1/users/:id
    Path parameter:
      - User ID.
    Return:
      - NULL if the User ID was deleted.
      - error 404 if the User ID doesn't exist.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """POST /api/v1/users/
    JSON body:
      - email.
      - password.
    """
    un = None
    error_msg = None
    try:
        un = request.get_json()
    except Exception as e:
        un = None
    if un is None:
        error_msg = "Wrong format"
    if error_msg is None and un.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and un.get("password", "") == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            user = User()
            user.email = un.get("email")
            user.password = un.get("password")
            user.first_name = un.get("first_name")
            user.last_name = un.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """PUT /api/v1/users/:id
    Path parameter:
      - User ID
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    un = None
    try:
        un = request.get_json()
    except Exception as e:
        un = None
    if un is None:
        return jsonify({'error': "Wrong format"}), 400
    if un.get('first_name') is not None:
        user.first_name = un.get('first_name')
    if un.get('last_name') is not None:
        user.last_name = un.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200