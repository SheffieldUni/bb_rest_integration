# MOLE URL and OAuth config.
# TODO: When we go live, replace these keys and don't check them into Git. 
BASE_URL = 'https://vle-staging.sheffield.ac.uk/learn/api/public'
OAUTH_URL = BASE_URL + '/v1/oauth2/token'
OAUTH_CLIENT_ID = ''
OAUTH_SECRET = ''
OAUTH_TIMEOUT = 3600

# Database config.
SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@localhost/bb_rest_integration'
SQLALCHEMY_TRACK_MODIFICATIONS = False
TRANSACTION_LOGGING = True

# API key for accessing the system.
API_KEY = ''

# Top-level element for XML bodies sent from SITS.
DATA_ELEMENT = 'data'

# Transform XML to JSON? 
TRANSFORM_XML = True


