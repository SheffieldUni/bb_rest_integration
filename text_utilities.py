import xmltodict 
import json
from xml.parsers.expat import ExpatError
from config import DATA_ELEMENT, DEFAULT_BODY

# Where all the magic translation happens. 
# Depends on a generic top level XML element
# in the request body--currently 'data'.
# TODO: We can also get the values we need with list(dict.values())[0],
# so do we need the name of the top element at all? 
def xml_to_json(xml):
	if xml == '':
		return xml
	try:
		dict = xmltodict.parse(xml)
	except ExpatError as e:
		# Something went wrong--probably malformed XML. Pass the
		# error back up to the caller. 
		raise ExpatError('Malformed XML - ' + str(e))
	
	# TODO: Error handling here? Can this go wrong?
	return json.dumps(dict[DATA_ELEMENT])
	
#TODO: Do we need a function to go JSON -> XML? 
