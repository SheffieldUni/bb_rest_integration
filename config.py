# MOLE URL and OAuth config.
# TODO: When we go live, replace these keys and don't check them into Git. 
BASE_URL = 'https://your-blackboard-url.ac.uk/learn/api/public'
OAUTH_URL = BASE_URL + '/v1/oauth2/token'
OAUTH_CLIENT_ID = 'your-blackboard-client-id'
OAUTH_SECRET = 'your-blackboard-secret'
OAUTH_TIMEOUT = 3600 # Blackboard OAuth tokens expire after an hour.

# Database config.
SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@localhost/bb_rest_integration'
SQLALCHEMY_TRACK_MODIFICATIONS = False
TRANSACTION_LOGGING = True

# API key for accessing the system.
# Insert this into the Authorization header when calling the APIs. 
API_KEY = 'long-random-string-change-me'

# Top-level element for XML bodies.
# This helps with extracting the data for JSON transformation.
DATA_ELEMENT = 'data'

# Transform XML to JSON? 
TRANSFORM_XML = True


