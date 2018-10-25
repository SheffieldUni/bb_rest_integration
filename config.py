# MOLE URL and OAuth config.
BASE_URL = 'https://sheffield-testmig2.blackboard.com/learn/api/public'
OAUTH_URL = BASE_URL + '/v1/oauth2/token'
OAUTH_CLIENT_ID = 'f973961c-e6bb-4485-859e-c1a6e578d554'
OAUTH_SECRET = 'fFNs2cB69giOptspx0rhrNcJ3w7lv0mq'
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

# Methods that don't have bodies. If we get one of these, 
# don't try to parse the nonexistent XML. 
BODILESS_METHODS = ['GET', 'DELETE']

