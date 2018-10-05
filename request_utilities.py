import xmltodict 
import json
from config import DATA_ELEMENT

# Where all the magic translation happens. 
# Depends on a generic top level XML element
# in the request body--currently 'data'.
# TODO: Make that configurable? 
def xml_to_json(xml):
	dict = xmltodict.parse(xml)
	return json.dumps(dict[DATA_ELEMENT])
	
#TODO: Do we need a function to go JSON -> XML? 