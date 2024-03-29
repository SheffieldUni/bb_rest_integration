# Main module for integrating with Blackboard's REST APIs.
# This exists because we had a system that didn't speak OAuth2 or JSON, and 
# the REST APIs need both. 

from flask import Flask, request, Response, make_response
import requests
from requests import RequestException
from xml.parsers.expat import ExpatError
from oauth import get_auth_headers
from text_utilities import xml_to_json
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, TRANSACTION_LOGGING
from config import BASE_URL, API_KEY
from config import TRANSFORM_XML



# Initialize our Flask app.
app = Flask(__name__)

# Database initialization. This needs to be below the app initialization 
# so our SQLAlchemy instance will bind to the app instance properly.  
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
from database_utilities import log_transaction, log_error


# Security check to see if our caller has sent along an API key.
# Without this, anyone could call these functions. As the decorator
# implies, this is called before every request is processed.
@app.before_request
def check_authorization():
	if request.headers.get('Authorization') != API_KEY:
		# Someone tried to get in without the right key. Return a "forbidden" response.
		error_msg = 'Invalid or missing API key.'
		log_error(request.path, request.method, error_msg, 403, request.data)
		return make_response(error_msg, 403)

# Custom error handler just in case someone tries to access an
# endpoint with the wrong method. 		
@app.errorhandler(405)
def method_not_allowed(e):
	error_msg = 'Method ' + request.method + ' not allowed for this endpoint.'
	log_error(request.path, request.method, error_msg, 405, request.data)
	return make_response(error_msg, 405)
	
# Central handler function for forwarding requests to Blackboard.
# There's a bit of magic going on here, so be sure to read the comments. 
def process_request(request):
	# This first bit gets the appropriate function from the requests library
	# based on the method used in the original request and assigns it to mole_request.
	# E.g., if the original request came in as a POST, mole_request becomes
	# requests.post(). The lower() call is because the the methods come in as
	# UPPERCASE, but need to be lowercase to match the method names in requests. 
	#
	# (Why "mole_request"? At the time, our Blackboard system was called 
	# MOLE--My Online Learning Environment.)
	try:
		mole_request = getattr(requests, request.method.lower())
	except AttributeError:
		# Someone sent us a method we don't recognize. Error out.
		# This shouldn't ever happen, but you can't be too careful.
		error_msg = 'Error getting handler for request method: ' + request.method
		log_error(request.path, request.method, error_msg, 500, request.data)
		return make_response(error_msg, 500)
	
	# This is where we do the actual get/post/etc. work. Request.path gets us the endpoint
	# from the original request, which we can just tack onto the base Blackboard URL. 
	#
	# The other two method calls handle getting our OAuth token and translating the
	# incoming XML to the JSON that the REST APIs expect. Then we return the HTTP response code to our caller. 
	try:
		if not request.data:
			# We've gotten a request (like a GET or DELETE) that doesn't have a body.
			# Make the request, but don't try to parse the nonexistent XML. 
			resp = mole_request(BASE_URL + request.path, headers=get_auth_headers())
		else:
			# Check to see if we're in an environment that sends XML instead of JSON. If so, transform it. 
			# Otherwise, just pass the JSON body on. 
			if TRANSFORM_XML:
				body = xml_to_json(request.data)
			else:
				body = request.data
			resp = mole_request(BASE_URL + request.path, headers=get_auth_headers(), data=body)
			
	except (RequestException, Exception) as e:
		# One of a number of possibilities went wrong in the request. 
		# (See http://docs.python-requests.org/en/master/_modules/requests/exceptions/ .) 
		# If we got a generic Exception, something else went wrong--most likely 
		# while getting an OAuth token. (See oauth.py .) 
		# Return an "internal server error" response.
		log_error(request.path, request.method, str(e), 500, request.data)
		return make_response('ERROR: ' + str(e), 500)
	except ExpatError as e:
		# We've been sent malformed XML. Return a "bad request" response. 
		log_error(request.path, request.method, str(e), 400, request.data)
		return make_response('Error in request body. ' + str(e), 400)

	# If we're here, everything went normally. Return our response body and code.
	if TRANSACTION_LOGGING:
		log_transaction(request.path, request.method, resp.status_code, request.data)
	return make_response(resp.content, resp.status_code)

	
# ----------- Routes	
#
# Everything below here is basically a wrapper around Blackboard's REST API endpoints. 
# They: 
# 1.) get a cached OAuth2 access token (or get a new one from Blackboard and cache it), 
# 2.) build the authorization headers for actually talking to Blackboard,  
# 3.) transform the XML we get from our caller into JSON, 
# 4.) send the JSON on to the right Blackboard endpoint with the right method, and 
# 5.) return the result to the caller. 


# --------------- USERS ---------------
@app.route('/v1/users', methods=['POST'])
def create_user():
	return process_request(request)

@app.route('/v1/users/userName:<userId>', methods=['DELETE', 'PATCH', 'GET'])
# PATCH = update, GET = query, DELETE = delete, obviously.
def user_operations(userId):
	return process_request(request)

# --------------- COURSES ---------------
@app.route('/v2/courses', methods=['POST'])
# Note the /v2--the v1 endpoint is deprecated.
def create_course():
	return process_request(request)

@app.route('/v2/courses/courseId:<courseId>', methods=['DELETE', 'PATCH', 'GET'])
# Methods do the same thing as user_operations, but on courses. 
def course_operations(courseId):
	return process_request(request)
	
# --------------- COURSE MEMBERSHIPS ---------------
@app.route('/v1/courses/courseId:<courseId>/users/userName:<userId>', methods=['PUT', 'PATCH', 'DELETE'])
# PUT = create course membership, PATCH = update, DELETE = delete.
def course_membership_operations(courseId, userId):
	return process_request(request)
	

	
