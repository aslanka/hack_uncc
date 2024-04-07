from __main__ import app

from bson.objectid import ObjectId
from Database.db import db
from flask import request, jsonify, send_file
import json
from utils import get_user
from werkzeug.utils import secure_filename
from gridfs import GridFS

fs = GridFS(db)
@app.route('/upload/image', methods=['POST'])
def upload_image():
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            filename = secure_filename(image.filename)
            image_id = fs.put(image, filename=filename)
            # image_id = fs.put(image.stream, filename=secure_filename(image.filename))
            return 'Image uploaded successfully: {}'.format(image_id)
        else:
            return 'Invalid image file'
    else:
        return 'No image part in the request'

@app.route('/upload/video', methods=['POST'])
def upload_video():
    if 'video' in request.files:
        video = request.files['video']
        if video.filename != '':
            filename = secure_filename(video.filename)
            video_id = fs.put(video, filename=filename)
            return 'Video uploaded successfully: {}'.format(str(video_id))
        else:
            return 'Invalid video file'
    else:
        return 'No video part in the request'

@app.route('/image/<image_id>', methods=['GET'])
def get_image(image_id):
    try:
        image_object = fs.get(ObjectId(image_id))
        if image_object:
            # Serve the image file
            return send_file(image_object, mimetype='image/jpeg')
        else:
            return jsonify({"error": "Image not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/video/<video_id>', methods=['GET'])
def get_video(video_id):
    try:
        fs = GridFS(db)
        video_object = fs.get(ObjectId(video_id))
        if video_object:
            # Serve the video file
            return send_file(video_object, mimetype='video/mp4')
        else:
            return jsonify({"error": "Video not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500