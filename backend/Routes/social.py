from __main__ import app
from Database.db import db
from flask import request, jsonify
import json
from utils import get_user



@app.route('/make_friend_request', methods=['POST'])
def friend_request():
    current_user_email = request.json['current_user_email']
    friend_email = request.json['friend_email']

    current_user = get_user(current_user_email)
    friend = get_user(friend_email)

    if current_user and friend:
        if friend_email in current_user.get('pending_friend_requests', []):
            return jsonify({"error": "Friend request already sent"}), 400

        current_user_pending_requests = current_user.get('pending_friend_requests', [])
        current_user_pending_requests.append(friend_email)
        current_user['pending_friend_requests'] = current_user_pending_requests
        db.Users.update_one({'email': current_user_email}, {'$set': {'pending_friend_requests': current_user_pending_requests}})


        friend_incoming_requests = friend.get('incoming_friend_requests', [])
        friend_incoming_requests.append(current_user_email)
        friend['incoming_friend_requests'] = friend_incoming_requests
        db.Users.update_one({'email': friend_email}, {'$set': {'incoming_friend_requests': friend_incoming_requests}})
        
        return jsonify({"message": "Friend request sent successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404




@app.route('/add_friend', methods=['POST'])
def add_friend():
    current_user_email = request.json['current_user_email']
    friend_email = request.json['friend_email']
    action = request.json['action']  # 'accept' or 'decline'

    current_user = get_user(current_user_email)
    friend = get_user(friend_email)

    if current_user and friend:
        if action == 'accept':
            # Add friend to current user's friends list
            current_user_friends = current_user.get('friends_list', [])
            if friend_email not in current_user_friends:
                current_user_friends.append(friend_email)
                current_user['friends_list'] = current_user_friends
                db.Users.update_one({'email': current_user_email}, {'$set': {'friends_list': current_user_friends}})
                
                # Remove friend request from current user's pending requests
                current_user_pending_requests = current_user.get('pending_friend_requests', [])
                if friend_email in current_user_pending_requests:
                    current_user_pending_requests.remove(friend_email)
                    current_user['pending_friend_requests'] = current_user_pending_requests
                    db.Users.update_one({'email': current_user_email}, {'$set': {'pending_friend_requests': current_user_pending_requests}})


                
                # Add current user to friend's friends list
                friend_friends = friend.get('friends_list', [])
                if current_user_email not in friend_friends:
                    friend_friends.append(current_user_email)
                    friend['friends_list'] = friend_friends
                    db.Users.update_one({'email': friend_email}, {'$set': {'friends_list': friend_friends}})
                    
                return jsonify({"message": "Friend added successfully"}), 200
            else:
                return jsonify({"error": "Friend already exists"}), 400
        elif action == 'decline':
            # Remove friend request from current user's pending requests
            current_user_pending_requests = current_user.get('pending_friend_requests', [])
            if friend_email in current_user_pending_requests:
                current_user_pending_requests.remove(friend_email)
                current_user['pending_friend_requests'] = current_user_pending_requests
                db.Users.update_one({'email': current_user_email}, {'$set': {'pending_friend_requests': current_user_pending_requests}})
                
                return jsonify({"message": "Friend request declined"}), 200
            else:
                return jsonify({"error": "Friend request not found"}), 404
        else:
            return jsonify({"error": "Invalid action"}), 400
    else:
        return jsonify({"error": "User not found"}), 404
    

@app.route('/get_pending_friend_requests', methods=['GET'])
def get_pending_friend_requests():
    current_user_email = request.json['current_user_email']

    current_user = get_user(current_user_email)

    if current_user:
        pending_requests = current_user.get('pending_friend_requests', [])
        return jsonify({"pending_requests": pending_requests}), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/get_incoming_friend_requests', methods=['GET'])
def get_incoming_friend_requests():
    current_user_email = request.json['current_user_email']

    current_user = get_user(current_user_email)

    if current_user:
        incoming_requests = current_user.get('incoming_friend_requests', [])
        return jsonify({"incoming_requests": incoming_requests}), 200
    else:
        return jsonify({"error": "User not found"}), 404