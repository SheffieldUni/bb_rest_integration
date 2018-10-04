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
from werkzeug.contrib.cache import SimpleCache

# Initialize our app, secret key, configuration, and database. 
app = Flask(__name__)
app.secret_key = "I_am_a_long_random_string_of_characters_not_really_change_me"
app.config.from_pyfile('config.py')
#db = SQLAlchemy(app)
cache = SimpleCache()


# Helper function to put together the headers for requests to MOLE. 
def format_auth_headers(token):
	return {'Authorization': 'Bearer ' + token,'Content-Type': 'application/json'}
	

# TODO: Replace caching mechanism. 
# TODO: Call this before every request? 
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
	#xmldata = request.data
	dict = xmltodict.parse(request.data)
	json_body = json.dumps(dict['user'])

	token = get_auth_token()
	headers = format_auth_headers(token)
	r = requests.post(app.config['BASE_URL'] + 'users', headers=headers, data=json_body)

	return str(r.status_code)

	
if __name__ == "__main__":
	app.run()