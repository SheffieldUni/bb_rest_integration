# Contains the classes for writing error/transaction records to the database
# as well as the functions to write them.

from mole_integration import app
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy(app)

class TransactionRecord(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	endpoint = db.Column(db.String(255), nullable=False)
	method = db.Column(db.String(10), nullable=False)
	timestamp = db.Column(db.DATETIME, nullable=False)
	status = db.Column(db.Integer, nullable=False)	
	xml_body = db.Column(db.TEXT, nullable=False)
	
	def __repr__(self):
		return '<TransactionRecord: %r>' % (self.endpoint + ' ' + self.response + ' ' + self.timestamp)	
		
class ErrorRecord(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	endpoint = db.Column(db.String(255), nullable=False)
	method = db.Column(db.String(10), nullable=False)	
	timestamp = db.Column(db.DATETIME, nullable=False)
	error_message = db.Column(db.String(120), nullable=False)
	status = db.Column(db.Integer, nullable=False)	
	xml_body = db.Column(db.TEXT, nullable=False)
	
	def __repr__(self):
		return '<TransactionRecord: %r>' % (self.endpoint + ' ' + self.response + ' ' + self.timestamp)	

def get_timestamp():
	return datetime.datetime.now()
		
def log_transaction(endpoint, method, status, xml_body):
	transaction = TransactionRecord(endpoint=endpoint, method=method, timestamp=get_timestamp(), status=status, xml_body=xml_body)
	db.session.add(transaction)
	db.session.commit()
	db.session.close()	
	
		
def log_error(endpoint, method, error_message, status, xml_body):
	error = ErrorRecord(endpoint=endpoint, method=method, timestamp=get_timestamp(), error_message=error_message, status=status, xml_body=xml_body)
	db.session.add(error)
	db.session.commit()
	db.session.close()	
	
