from __main__ import app
from bson import ObjectId
from flask import request, jsonify
from Database.db import db


@app.route('/challenges', methods=['GET'])
def get_challenges():
    email = request.args.get('email')
    challenge_type = request.args.get('type')

    if challenge_type == 'forYou':
        challenges = db.Challenges.find()
    elif challenge_type == 'friends':
        user = db.Users.find_one({'email': email})
        if user:
            friend_emails = user.get('friends_list', [])
            challenges = db.Challenges.find({'createdBy': {'$in': friend_emails}})
        else:
            challenges = []
    else:
        challenges = []

    challenge_list = []
    for challenge in challenges:
        challenge_list.append({
            '_id': str(challenge['_id']),
            'title': challenge['title'],
            'image': challenge['image'],
            'subscribed': email in challenge.get('subscribers', []),
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

@app.route('/create_challenge', methods=['POST'])
def create_challenge():
    title = request.json['title']
    image = request.json['image']
    email = request.json['email']

    challenge = db.Challenges.find_one({'title': title})
    if challenge:
        db.Challenges.update_one(
            {'_id': challenge['_id']},
            {'$addToSet': {'subscribers': email}}
        )
        return jsonify({'message': 'Subscribed to existing challenge'}), 200
    else:
        new_challenge = {
            'title': title,
            'image': image,
            'createdBy': email,
            'subscribers': [email],
        }
        db.Challenges.insert_one(new_challenge)
        return jsonify({'message': 'New challenge created'}), 201