import xmltodict 
import json
from xml.parsers.expat import ExpatError
from config import DATA_ELEMENT

def is_json(body):
	# Helper method to check the body for JSON first, just in case someone got 
	# clever and pre-transformed the body before calling us. If it parses
	# as JSON, just hand it back. 
	json_body = None
	try:
		json.loads(str(body))
		print("That was JSON.") 
		json_body = True
	except ValueError:
		# Oops. That wasn't JSON. 
		print("That wasn't JSON.")
		json_body = False
	
	return json_body

# Where all the magic translation happens. 
# Depends on a generic top level XML element
# in the request body--currently 'data'.
# TODO: We can also get the values we need with list(dict.values())[0],
# so do we need the name of the top element at all? 
def xml_to_json(body):
	if not is_json(body):
		try:
			dict = xmltodict.parse(body)
		except ExpatError as e:
			# Something went wrong--probably malformed XML. Pass the
			# error back up to the caller. 
			raise ExpatError('Malformed XML - ' + str(e))
		
		# TODO: Error handling here? Can this go wrong?
		return json.dumps(dict[DATA_ELEMENT])
	
#TODO: Do we need a function to go JSON -> XML? 
