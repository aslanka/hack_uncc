from __main__ import app

from bson.objectid import ObjectId
from Database.db import db
from flask import request, jsonify, send_file
import json
from utils import get_user
from werkzeug.utils import secure_filename
from gridfs import GridFS
import base64

fs = GridFS(db)
@app.route('/upload/image', methods=['POST'])
def upload_image():
    try:
        # Get challenge_id from the request body or URL parameters
        challenge_id = request.form.get('challenge_id')
        if not challenge_id:
            return jsonify({"error": "Challenge ID is required"}), 400

        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                # Save image to GridFS
                filename = secure_filename(image.filename)
                image_id = fs.put(image, filename=filename)
                # Associate image with challenge by updating challenge document in MongoDB
                db.Challenges.update_one({'_id': ObjectId(challenge_id)}, {'$push': {'images': str(image_id)}})
                return jsonify({"message": "Image uploaded successfully", "image_id": str(image_id)})
            else:
                return jsonify({"error": "Invalid image file"}), 400
        else:
            return jsonify({"error": "No image part in the request"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/upload/video', methods=['POST'])
def upload_video():
    try:
        # Get challenge_id from the request body or URL parameters
        challenge_id = request.form.get('challenge_id')
        if not challenge_id:
            return jsonify({"error": "Challenge ID is required"}), 400

        if 'video' in request.files:
            video = request.files['video']
            if video.filename != '':
                # Save video to GridFS
                filename = secure_filename(video.filename)
                video_id = fs.put(video, filename=filename)
                # Associate video with challenge by updating challenge document in MongoDB
                db.Challenges.update_one({'_id': ObjectId(challenge_id)}, {'$push': {'videos': str(video_id)}})
                return jsonify({"message": "Video uploaded successfully", "video_id": str(video_id)})
            else:
                return jsonify({"error": "Invalid video file"}), 400
        else:
            return jsonify({"error": "No video part in the request"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/images/<challenge_id>', methods=['GET'])
def get_images_by_challenge_id(challenge_id):
    try:
        # Retrieve list of image IDs associated with the given challenge ID
        challenge = db.Challenges.find_one({'_id': ObjectId(challenge_id)})
        if challenge:
            images = challenge.get('images', [])
            if images:
                image_data = []
                for image_id in images:
                    image_object = fs.get(ObjectId(image_id))
                    if image_object:
                        # Return image file using send_file
                        return send_file(image_object, mimetype='image/jpeg')
                return jsonify({"error": "No images found for this challenge"}), 404
            else:
                return jsonify({"error": "No images found for this challenge"}), 404
        else:
            return jsonify({"error": "Challenge not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @app.route('/videos/<challenge_id>', methods=['GET'])
# def get_videos_by_challenge_id(challenge_id):
#     try:
#         # Retrieve list of video IDs associated with the given challenge ID
#         challenge = db.Challenges.find_one({'_id': ObjectId(challenge_id)})
#         if challenge:
#             videos = challenge.get('videos', [])
#             return jsonify({"videos": videos})
#         else:
#             return jsonify({"error": "Challenge not found"}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@app.route('/videos/<challenge_id>', methods=['GET'])
def get_videos_by_challenge_id(challenge_id):
    try:
        # Retrieve list of video IDs associated with the given challenge ID
        challenge = db.Challenges.find_one({'_id': ObjectId(challenge_id)})
        if challenge:
            videos = challenge.get('videos', [])
            if videos:
                # Retrieve and send the first video file associated with the challenge
                video_id = videos[0]  # Assuming you want to send the first video
                video_object = fs.get(ObjectId(video_id))
                return send_file(video_object, mimetype='video/mp4')
            else:
                return jsonify({"error": "No videos found for this challenge"}), 404
        else:
            return jsonify({"error": "Challenge not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500