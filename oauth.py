from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from config import OAUTH_CLIENT_ID,OAUTH_SECRET,OAUTH_URL, OAUTH_TIMEOUT
#from database_utilities import log_error
# This Redis cache can be swapped out. 
from werkzeug.contrib.cache import RedisCache
cache = RedisCache()

# Helper function to put together the proper headers for requests to MOLE. 
def get_auth_headers():
	return {'Authorization': 'Bearer ' + get_auth_token(),'Content-Type': 'application/json'}
	

# Get a cached OAuth2 token, or a new one from MOLE if the current token's expired. 
def get_auth_token():
	access_token = cache.get('access_token')
	if access_token is None:
		try:
			print('Getting new token.')
			auth = HTTPBasicAuth(OAUTH_CLIENT_ID, OAUTH_SECRET)
			client = BackendApplicationClient(client_id=OAUTH_CLIENT_ID)
			oauth = OAuth2Session(client=client)
			token = oauth.fetch_token(token_url=OAUTH_URL, auth=auth)
			access_token = token['access_token']
			cache.set('access_token', access_token, timeout=OAUTH_TIMEOUT)
		except Exception as e:
			# Uh-oh. Something's gone wrong. Log the error, then 
			# return None and let our caller finish handling the 
			# whole thing. 
			#log_error("OAuth token request", str(e), 500, '')
			access_token = None
			
	return access_token