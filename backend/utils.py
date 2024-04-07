from Database.db import db
from flask import request, jsonify

def get_user(email):
    user = db.Users.find_one({"email": email})
    if user:
        return dict(user)  # Ensure it's a dictionary
    else:
        return {}  # Return an empty dictionary if user is not found
