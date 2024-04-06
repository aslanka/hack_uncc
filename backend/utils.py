from Database.db import db
from flask import request, jsonify

def get_user(email):
    user = db.Users.find_one({'email': email})
    if user:
        return user
    else:
        return jsonify({'error': 'User not found'}), 404