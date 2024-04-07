from __main__ import app
from bson import ObjectId
from flask import request, jsonify
from Database.db import db


@app.route('/challenges', methods=['GET'])
def get_challenges():
    email = request.args.get('email')
    challenge_type = request.args.get('type')

    friend_emails = []
    if challenge_type == 'friends':
        user = db.Users.find_one({'email': email})
        if user:
            friend_emails = user.get('friends_list', [])
        challenges = db.Challenges.find({'$or': [{'createdBy': {'$in': friend_emails}}, {'subscribers': email}]})
    elif challenge_type == 'forYou':
        challenges = db.Challenges.find()
    else:
        challenges = []

    challenge_list = []
    for challenge in challenges:
        subscribed_friends = [friend for friend in challenge.get('subscribers', []) if friend in friend_emails]
        challenge_list.append({
            '_id': str(challenge['_id']),
            'title': challenge['title'],
            'subscribed': email in challenge.get('subscribers', []),
            'subscribedFriends': subscribed_friends,
        })

    return jsonify({'challenges': challenge_list}), 200



@app.route('/subscribe_challenge', methods=['POST'])
def subscribe_challenge():
    email = request.json['email']
    challenge_id = request.json['challengeId']

    db.Challenges.update_one(
        {'_id': ObjectId(challenge_id)},
        {'$addToSet': {'subscribers': email}}
    )

    return jsonify({'message': 'Subscribed to challenge'}), 200

@app.route('/toggle_subscribe_challenge', methods=['POST'])
def toggle_subscribe_challenge():
    email = request.json['email']
    challenge_id = request.json['challengeId']

    challenge = db.Challenges.find_one({'_id': ObjectId(challenge_id)})
    if challenge:
        if email in challenge.get('subscribers', []):
            db.Challenges.update_one(
                {'_id': ObjectId(challenge_id)},
                {'$pull': {'subscribers': email}}
            )
            message = 'Unsubscribed from challenge'
        else:
            db.Challenges.update_one(
                {'_id': ObjectId(challenge_id)},
                {'$addToSet': {'subscribers': email}}
            )
            message = 'Subscribed to challenge'
    else:
        message = 'Challenge not found'

    return jsonify({'message': message}), 200


@app.route('/create_challenge', methods=['POST'])
def create_challenge():
    title = request.json['title']
    image = request.json['image']
    email = request.json['email']

    challenge = db.Challenges.find_one({'title': title})
    if challenge:
        # Check if user is already subscribed
        if email not in challenge.get('subscribers', []):
            db.Challenges.update_one(
                {'_id': challenge['_id']},
                {'$addToSet': {'subscribers': email}}
            )
            message = 'Subscribed to existing challenge'
        else:
            message = 'Already subscribed to this challenge'
    else:
        new_challenge = {
            'title': title,
            'image': image,
            'createdBy': email,
            'subscribers': [email],
        }
        db.Challenges.insert_one(new_challenge)
        message = 'New challenge created and subscribed'

    return jsonify({'message': message}), 200
