import requests
from base64 import b64encode
import json
from config import OAUTH_CLIENT_ID, OAUTH_SECRET, OAUTH_URL, OAUTH_TIMEOUT
# This Redis cache can be swapped out with other supported caches. 
from werkzeug.contrib.cache import RedisCache

# Initialize our cache.
# TODO: Set up password authentication for some extra security. 
cache = RedisCache(default_timeout=OAUTH_TIMEOUT)

# Helper function to put together the proper headers for requests to Blackboard. 
def get_auth_headers():
	return {'Authorization': 'Bearer ' + get_auth_token(), 'Content-Type': 'application/json'}
	

# Get a cached OAuth2 token, or a new one from Blackboard if the current token's expired. 
def get_auth_token():
	access_token = cache.get('access_token')
	if access_token is None:
		try:
			# First encode our credentials. The standard expects a base64-encoded string of the 
			# key and secret separated by a colon--'key:secret'. The encode and decode calls 
			# are because we need to send a string, but b64encode works on bytes. Irritating.
			encoded_credentials = b64encode( (OAUTH_CLIENT_ID + ':' + OAUTH_SECRET).encode() ).decode()
			
			# Add 'Basic' on to form the rest of our header content, then post our request to the 
			# auth URL. Note the grant_type body field--this has to be set or the request won't work.
			authorization = 'Basic ' + encoded_credentials
			resp = requests.post(OAUTH_URL, headers={'Authorization':authorization}, data={'grant_type':'client_credentials'})
			
			#Finally, grab the access token from the returned JSON and cache it. 
			access_token = json.loads(resp.text)['access_token']
			cache.set('access_token', access_token)
		except Exception as e:
			# Uh-oh. Something's gone wrong. Re-raise our exception.
			# NB: Throwing around generic Exceptions is kind of terrible, 
			# but the exception hierarchy of everything above is tangled and
			# also terrible. Let's just catch everything. 
			raise Exception(str(e))
			
	return access_token
