# MOLE URL and OAuth config.
# TODO: When we go live, replace these keys and don't check them into Git. 
BASE_URL = 'https://vle-staging.sheffield.ac.uk/learn/api/public'
OAUTH_URL = BASE_URL + '/v1/oauth2/token'
OAUTH_CLIENT_ID = '1509cc57-d0a9-47e7-b622-c04637bb3fbc'
OAUTH_SECRET = '1WyvdgV9ZcZwZFzP3vQxUxsUUAtOFUPN'
OAUTH_TIMEOUT = 3600

# Database config.
SQLALCHEMY_DATABASE_URI = 'mysql://mole_integration:mole@localhost/mole_integration'
SQLALCHEMY_TRACK_MODIFICATIONS = False
TRANSACTION_LOGGING = True

# API key for accessing the system.
# TODO: Make this an actual secure key before you move to production. Duh.
API_KEY = '8675309'

# Top-level element for XML bodies sent from SITS.
DATA_ELEMENT = 'data'


