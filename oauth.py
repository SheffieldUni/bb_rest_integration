from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from config import OAUTH_CLIENT_ID,OAUTH_SECRET,OAUTH_URL, OAUTH_TIMEOUT
# This Redis cache can be swapped out. 
from werkzeug.contrib.cache import RedisCache
cache = RedisCache()

# Helper function to put together the proper headers for requests to MOLE. 
def get_auth_headers():
	return {'Authorization': 'Bearer ' + get_auth_token(),'Content-Type': 'application/json'}
	

# Get a cached OAuth2 token, or a new one from MOLE if the current token's expired. 
# TODO: Error handling. Log getting new token?
# Thought: catch the error, log it, return None, and let the caller error handling 
# take care of everything. Slightly neater, possibly. 
def get_auth_token():
	access_token = cache.get('access_token')
	if access_token is None:
		print('Getting new token.')
		auth = HTTPBasicAuth(OAUTH_CLIENT_ID, OAUTH_SECRET)
		client = BackendApplicationClient(client_id=OAUTH_CLIENT_ID)
		oauth = OAuth2Session(client=client)
		token = oauth.fetch_token(token_url=OAUTH_URL, auth=auth)
		access_token = token['access_token']
		cache.set('access_token', access_token, timeout=OAUTH_TIMEOUT)
		
	return access_token