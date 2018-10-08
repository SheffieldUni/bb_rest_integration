from flask import Flask, request, Response
import requests
from oauth import get_auth_headers
from request_utilities import xml_to_json
from config import BASE_URL, API_KEY
#TODO: Replace this with a better cache. This most likely isn't thread-safe. 
# Memcache? Filesystem? UWSGI?
from werkzeug.contrib.cache import SimpleCache

# Initialize our app, secret key, and cache. 
app = Flask(__name__)
#app.secret_key = "I_am_a_long_random_string_of_characters_not_really_change_me"
cache = SimpleCache()


# ----------- Routes	

# Check to see if our caller has sent along an API key.
# Without this, anyone could call these functions. 
@app.before_request
def check_authorization():
	if request.headers.get('Authorization') != API_KEY:
		return Response(status=403)


# TODO: Store the rest of the routes (e.g., 'users') in a database table or move them to the config file.

@app.route('/user/create', methods=['POST'])
def create_user():
	r = requests.post(BASE_URL + 'users', headers=get_auth_headers(cache), data=xml_to_json(request.data))
	return str(r.status_code)

@app.route('/user/delete/<userId>', methods=['DELETE'])
def delete_user(userId):
	r = requests.delete(BASE_URL + 'users/userName:' + userId, headers=get_auth_headers(cache), data=xml_to_json(request.data))
	return str(r.status_code)
	
@app.route('/course/<courseId>/enrol/user/<userId>', methods=['PUT'])
def enrol_user(courseId, userId):
	print(BASE_URL + 'courses/courseId:' + courseId + '/users/userName:' + userId)
	r = requests.put(BASE_URL + 'courses/courseId:' + courseId + '/users/userName:' + userId, headers=get_auth_headers(cache), data=xml_to_json(request.data))
	return str(r.status_code)
	
@app.route('/course/update/<courseId>/user/<userId>', methods=['PATCH'])
def update_user(courseId, userId):
	print(BASE_URL + 'courses/courseId:' + courseId + '/users/userName:' + userId)
	r = requests.patch(BASE_URL + 'courses/courseId:' + courseId + '/users/userName:' + userId, headers=get_auth_headers(cache), data=xml_to_json(request.data))
	return str(r.status_code)	