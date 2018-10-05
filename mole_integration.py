from flask import Flask, request
import requests
from oauth import get_auth_headers
from request_utilities import xml_to_json
from config import BASE_URL
#TODO: Replace this with a better cache. This most likely isn't thread-safe. 
# Memcache? Filesystem? UWSGI?
from werkzeug.contrib.cache import SimpleCache

# Initialize our app, secret key, and cache. 
app = Flask(__name__)
#app.secret_key = "I_am_a_long_random_string_of_characters_not_really_change_me"
cache = SimpleCache()


# ----------- Routes	

# TODO: Store the rest of the route ('users') in a database table or move it to the config file.
@app.route('/user/create', methods=['POST'])
def create_user():
	r = requests.post(BASE_URL + 'users', headers=get_auth_headers(cache), data=xml_to_json(request.data))
	return str(r.status_code)
