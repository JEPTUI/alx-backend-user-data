#!/usr/bin/env python3
"""Basic Flask app
"""
from flask import Flask, request, jsonify, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def welcome():
    """Flask app GET method
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    """Register users
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        user = AUTH.register_user(email, password)

        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Implements the login function
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response(
                jsonify({"email": email, "message": "logged in"}))
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)

    if user:
        AUTH.destroy_session(user.id)

        return redirect('/')
    else:
        abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
