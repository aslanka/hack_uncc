from __main__ import app
from flask import request, jsonify
import json
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from Database.db import db











@app.route('/register', methods=['POST'])
def register():
    email = request.json['email']
    password = request.json['password']


    user = db.Users.find_one({'email': email})
    if user:
        return jsonify({'error': 'User already exists'}), 409
    hashed_password = generate_password_hash(password)
        # Save the user and then create a token with more information
    user = {
            'email': email,
            'password': hashed_password,
        }
    db.Users.insert_one(user)
    # user_from_db = db.Users.find_one({'email': email})
    # token = jwt.encode({
    #     'user_id': str(user_from_db['_id']),
    #     'email': email,
    #     'name': user['name'],
    #     'exp': datetime.utcnow() + timedelta(minutes=30)
    #     }, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({"message": "registed"}), 200


@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    user = db.Users.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        return jsonify({"token": "successfull"}), 200
    else:
        return jsonify({'error': 'Invalid login credentials'}), 400