import sqlite3
from flask import (
  Blueprint, request, jsonify, redirect, url_for, session
)
# from werkzeug.security import safe_str_cmp
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
# from datetime import timedelta

user = Blueprint('user', __name__)
# CORS(user)

# @user.before_request
# def make_session_permanent():
#     session.permanent = True
#     user.permanent_session_lifetime = timedelta(minutes=5)

# USER RESOURCE
@user.route('/signup', methods=["POST"])
def signup():
    if request.is_json:
        data = request.get_json()
        bcrypt = Bcrypt()
        pw_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "INSERT INTO {table} VALUES (NULL, ?, ?, ?, ?)".format(table='users')
            
            cursor.execute(query, (data['username'], pw_hash, data['first_name'], data['last_name']))

            connection.commit()
            connection.close()
            # return redirect(url_for('user.login')), 302
            return jsonify(
                message = "Successful signup.  Login redirect."
            )
        except sqlite3.Error as e:
            print(e.args[0])
            return jsonify(
                error = "Invalid signup.  Username is already taken.  Please try again.",
            ), 400
    else:
        return jsonify(
            error = "The request payload is not in JSON format."
        ), 400

@user.route('/login', methods=['POST'])
# @cross_origin(expose_headers=['Set-Cookie'])
def login():
    if request.is_json:
        # get user from database using username and then check credentials
        data = request.get_json()
        bcrypt = Bcrypt()

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM {table} WHERE username=?".format(table='users')
        result = cursor.execute(query, (data['username'],))
        user = result.fetchone()

        if user:
            if bcrypt.check_password_hash(user[2], data['password']):
                # password comparison success
                session['user_id'] = user[0]
                session.permanent = True
                return jsonify(
                    message = "Successfully logged in."
                ), 200
                # return session['user_id'], 200
            return jsonify(
                message = "Invalid credentials.  Please try again."
            ), 400
    return jsonify(
      message = "Credentials are invalid and/or not in JSON format."
    )

@user.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify(
        message = 'You have successfully logged out.'
    ), 200


# test endpoint
@user.route('/users', methods=['GET'])
def get_users():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    query = "SELECT * FROM {table}".format(table="users")
    response = cursor.execute(query)

    user_lst = []

    for row in response:
        user_lst.append({
            'id': row[0],
            'username': row[1],
            'password': row[2],
            'first_name': row[3],
            'last_name': row[4]
        })
    
    connection.close()
    
    if user_lst:
        return jsonify(
            users = user_lst
        )
    return jsonify(
        message = 'No users found'
    )

