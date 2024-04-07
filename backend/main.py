from flask import Flask, request, abort
from flask_cors import CORS


app = Flask(__name__, static_url_path='', 
            static_folder='Tests',)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={r"/*": {"origins": ["http://localhost:8080", "*", " http://localhost:8081", "https://expo.saipriya.org"]}})



# Update CORS configuration to include the new origin

import Routes.auth
import Routes.social
import Routes.feed
import Routes.media_upload
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
