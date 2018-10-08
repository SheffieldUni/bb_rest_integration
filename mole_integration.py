from flask import Flask, request, Response
import requests
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
	

# ----------- Routes	
#
# Everything below here is basically a wrapper around Blackboard's REST API endpoints. 
# Why? Because SITS doesn't currently speak OAuth2 or JSON, and MOLE needs both of those
# when you're calling the API. What these do is 1.) get an OAuth2 access token (or
# use a cached one), 2.) build the authorization headers for talking to MOLE, and 3.) transform
# the XML we'll be getting into JSON. It should be relatively quick, but we'll see. 

@app.route('/users', methods=['POST'])
def create_user():
	r = requests.post(BASE_URL + request.path, headers=get_auth_headers(), data=xml_to_json(request.data))
	return str(r.status_code)


@app.route('/users/userName:<userId>', methods=['DELETE'])
def delete_user(userId):
	r = requests.delete(BASE_URL + request.path, headers=get_auth_headers(), data=xml_to_json(request.data))
	return str(r.status_code)
	
@app.route('/courses/courseId:<courseId>/users/userName:<userId>', methods=['PUT'])
def enrol_user(courseId, userId):
	r = requests.put(BASE_URL + request.path, headers=get_auth_headers(), data=xml_to_json(request.data))
	return str(r.status_code)
	
@app.route('/courses/courseId:<courseId>/users/userName:<userId>', methods=['PATCH'])	
def update_user(courseId, userId):
	r = requests.patch(BASE_URL + request.path, headers=get_auth_headers(), data=xml_to_json(request.data))
	return str(r.status_code)	
	
