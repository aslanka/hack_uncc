from flask import Flask, request, abort


app = Flask(__name__, static_url_path='', 
            static_folder='Tests',)


# Update CORS configuration to include the new origin

import Routes.auth
import Routes.social
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
