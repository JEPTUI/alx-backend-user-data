#!/usr/bin/env python3
"""Creates a new flask view that handles
all routes for the Session authentication
"""

from flask import Flask, jsonify, request, make_response
from api.v1.views import app_views
from api.v1.views.users import User
from api.v1.app import auth
from api.v1.app import app
from api.v1.auth.session_auth import SessionAuth


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Handles all routes
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user[0].id)
    user_data = user[0].to_json()

    session_cookie_name = app.config.get('SESSION_NAME', '_my_session_id')
    response = make_response(jsonify(user_data))
    response.set_cookie(session_cookie_name, session_id)

    return response


@app_views.route(
        '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """logouts a session
    """
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
