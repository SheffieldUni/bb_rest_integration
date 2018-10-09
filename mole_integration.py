from flask import Flask, request, Response, make_response
import requests
from requests import RequestException
from xml.parsers.expat import ExpatError
from oauth import get_auth_headers
from text_utilities import xml_to_json
from config import BASE_URL, API_KEY

# Initialize our app.
app = Flask(__name__)


# Security check to see if our caller has sent along an API key.
# Without this, anyone could call these functions. 
@app.before_request
def check_authorization():
	if request.headers.get('Authorization') != API_KEY:
		return Response(status=403)
	
# Central handler function for forwarding requests to MOLE.
# There's a bit of magic going on here, so be sure to read the comments. 
# TODO: Logging. Separate module?  
def process_request(request):
	# This first bit gets the appropriate function from the requests library
	# based on the method used in the original request and assigns it to mole_request.
	# E.g., if the original request came in as a POST, mole_request becomes
	# requests.post(). The lower() call is because the the methods come in as
	# UPPERCASE, but need to be lowercase to match the method names in requests. 
	try:
		mole_request = getattr(requests, request.method.lower())
	except AttributeError:
		# Someone sent us a method we don't recognize. This *should* never happen,
		# but you can't be too careful. Error out.
		# TODO: Log this. 
		return make_response('Error getting handler for request method: ' + request.method,  500)
	
	# This is where we do the actual get/post/etc. The beauty of copying the 
	# Blackboard endpoint structure is that we can just tack 
	# request.path (which holds the route--e.g., '/users' onto the MOLE base 
	# URL without having to construct the endpoint manually. 
	#
	# The other two method calls handle getting our OAuth token and translating the
	# incoming XML to the JSON that MOLE expects. Then we return the HTTP response code to our caller. 
	try:
		resp = mole_request(BASE_URL + request.path, headers=get_auth_headers(), data=xml_to_json(request.data))
	except RequestException as e:
		# One of a number of possibilities went wrong. (See http://docs.python-requests.org/en/master/_modules/requests/exceptions/ .) 
		# Error out. 
		# TODO: Log this too. 
		return make_response('ERROR: ' + str(e), 500)
	except ExpatError as e:
		# We've been sent malformed XML. Send a "bad request" response back. 
		# TODO: Yep, log this one too.
		return make_response('Error in request body. ' + str(e), 400)
	
	# If we're here, everything went normally. Return our response code.
	return str(resp.status_code)

	
# ----------- Routes	
#
# Everything below here is basically a wrapper around Blackboard's REST API endpoints. 
# Why? Because SITS doesn't currently speak OAuth2 or JSON, and MOLE needs both of those
# when you're calling the API. What these do is 1.) get an OAuth2 access token (or
# use a cached one), 2.) build the authorization headers for talking to MOLE, and 3.) transform
# the XML we'll be getting into JSON. It should be relatively quick, but we'll see. 

@app.route('/users', methods=['POST'])
def create_user():
	return process_request(request)

@app.route('/users/userName:<userId>', methods=['DELETE'])
def delete_user(userId):
	return process_request(request)
	
@app.route('/courses/courseId:<courseId>/users/userName:<userId>', methods=['PUT', 'PATCH'])
def enrol_or_update_user(courseId, userId):
	return process_request(request)
	
