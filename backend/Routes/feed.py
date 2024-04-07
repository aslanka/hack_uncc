from __main__ import app
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from gridfs import GridFS
from bson import ObjectId
from Database.db import db

fs = GridFS(db)


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
        image_ids = challenge.get('images', [])[:6]  # Limit to top 6 images
        challenge_list.append({
            '_id': str(challenge['_id']),
            'title': challenge['title'],
            'subscribed': email in challenge.get('subscribers', []),
            'subscribedFriends': subscribed_friends,
            'images': image_ids,
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
    title = request.form['title']
    email = request.form['email']
    image = request.files.get('image')

    if not title or not email:
        return jsonify({'error': 'Title and email are required'}), 400

    # Check if a challenge with the same title already exists
    existing_challenge = db.Challenges.find_one({'title': title})

    if existing_challenge:
        # Challenge exists, add the image to the existing challenge
        if image:
            filename = secure_filename(image.filename)
            image_id = fs.put(image, filename=filename)
            db.Challenges.update_one(
                {'_id': existing_challenge['_id']},
                {'$push': {'images': str(image_id)}}
            )
        return jsonify({
            'message': 'Image added to existing challenge',
            'challengeId': str(existing_challenge['_id']),
            'imageId': str(image_id) if image else None
        }), 200
    else:
        # Challenge does not exist, create a new challenge
        challenge = {
            'title': title,
            'createdBy': email,
            'subscribers': [email],
            'images': []
        }
        challenge_id = db.Challenges.insert_one(challenge).inserted_id

        if image:
            filename = secure_filename(image.filename)
            image_id = fs.put(image, filename=filename)
            db.Challenges.update_one(
                {'_id': challenge_id},
                {'$push': {'images': str(image_id)}}
            )

        return jsonify({
            'message': 'New challenge created',
            'challengeId': str(challenge_id),
            'imageId': str(image_id) if image else None
        }), 201
    title = request.form['title']
    email = request.form['email']
    # You should have authentication in place to get the email, this is just for example
    image = request.files.get('image')

    # Validation (if title or email is empty, return an error)
    if not title or not email:
        return jsonify({'error': 'Title and email are required'}), 400

    challenge = {
        'title': title,
        'createdBy': email,
        'subscribers': [email],
        'images': []
    }
    challenge_id = db.Challenges.insert_one(challenge).inserted_id

    if image:
        filename = secure_filename(image.filename)
        image_id = fs.put(image, filename=filename)
        db.Challenges.update_one(
            {'_id': challenge_id},
            {'$push': {'images': str(image_id)}}
        )

    return jsonify({
        'message': 'Challenge created',
        'challengeId': str(challenge_id),
        'imageId': str(image_id) if image else None
    }), 201