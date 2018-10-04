from flask import Flask, request, Response
#from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import timedelta
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import xmltodict 
import json

#TODO: Replace this with a better cache. This most likely isn't thread-safe. 
# Memcache? Filesystem? UWSGI?
from werkzeug.contrib.cache import SimpleCache

# Initialize our app, secret key, configuration, and database. 
app = Flask(__name__)
app.secret_key = "I_am_a_long_random_string_of_characters_not_really_change_me"
app.config.from_pyfile('config.py')
#db = SQLAlchemy(app)
cache = SimpleCache()

# Where all the magic translation happens. 
# Depends on a generic top level XML element
# in the request body--currently 'data'.
# TODO: Make that configurable? 
def xml_to_json(xml):
	dict = xmltodict.parse(xml)
	return json.dumps(dict['data'])

# Helper function to put together the headers for requests to MOLE. 
def get_auth_headers():
	return {'Authorization': 'Bearer ' + get_auth_token(),'Content-Type': 'application/json'}
	

# Get a cached OAuth2 token, or a new one from MOLE if the current token's expired. 
# TODO: Replace caching mechanism. See above re: SimpleCache.
def get_auth_token():
	access_token = cache.get('access_token')
	if access_token is None:
		print('Getting new token.')
		auth = HTTPBasicAuth(app.config['OAUTH_CLIENT_ID'], app.config['OAUTH_SECRET'])
		client = BackendApplicationClient(client_id=app.config['OAUTH_CLIENT_ID'])
		oauth = OAuth2Session(client=client)
		token = oauth.fetch_token(token_url=app.config['OAUTH_URL'], auth=auth)
		access_token = token['access_token']
		cache.set('access_token', access_token, timeout=3600)
	else:
		print('Using cached token.')
		
	return access_token


# ----------- Routes	

# TODO: Store the rest of the route ('users') in a database table or move it to the config file.
@app.route('/user/create', methods=['POST'])
def create_user():
	r = requests.post(app.config['BASE_URL'] + 'users', headers=get_auth_headers(), data=xml_to_json(request.data))
	return str(r.status_code)

	
if __name__ == "__main__":
	app.run()