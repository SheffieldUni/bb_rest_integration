from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from config import OAUTH_CLIENT_ID,OAUTH_SECRET,OAUTH_URL, OAUTH_TIMEOUT

# Helper function to put together the headers for requests to MOLE. 
# TODO: Passing the cache into this function just to pass it on to get_auth_token is
# kind of ugly. How to rework that? 
def get_auth_headers(cache):
	return {'Authorization': 'Bearer ' + get_auth_token(cache),'Content-Type': 'application/json'}
	

# Get a cached OAuth2 token, or a new one from MOLE if the current token's expired. 
# TODO: Replace caching mechanism. See above re: SimpleCache.
def get_auth_token(cache):
	access_token = cache.get('access_token')
	if access_token is None:
		print('Getting new token.')
		auth = HTTPBasicAuth(OAUTH_CLIENT_ID, OAUTH_SECRET)
		client = BackendApplicationClient(client_id=OAUTH_CLIENT_ID)
		oauth = OAuth2Session(client=client)
		token = oauth.fetch_token(token_url=OAUTH_URL, auth=auth)
		access_token = token['access_token']
		cache.set('access_token', access_token, timeout=3600)
	else:
		print('Using cached token.')
		
	return access_token