from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from config import OAUTH_CLIENT_ID, OAUTH_SECRET, OAUTH_URL, OAUTH_TIMEOUT
# This Redis cache can be swapped out with other supported caches. 
from werkzeug.contrib.cache import RedisCache
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
			print('Getting new token.')
			auth = HTTPBasicAuth(OAUTH_CLIENT_ID, OAUTH_SECRET)
			client = BackendApplicationClient(client_id=OAUTH_CLIENT_ID)
			oauth = OAuth2Session(client=client)
			token = oauth.fetch_token(token_url=OAUTH_URL, auth=auth)
			access_token = token['access_token']
			cache.set('access_token', access_token)
		except Exception as e:
			# Uh-oh. Something's gone wrong. Re-raise our exception.
			# NB: Throwing around generic Exceptions is kind of terrible, 
			# but the exception hierarchy of everything above is tangled and
			# also terrible. Let's just catch everything. 
			raise Exception(str(e))
			
	return access_token
