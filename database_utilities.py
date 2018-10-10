from mole_integration import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class TransactionRecord(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	endpoint = db.Column(db.String(255), nullable=False)
	timestamp = db.Column(db.DATETIME, nullable=False)
	status = db.Column(db.Integer, nullable=False)	
	xml_body = db.Column(db.TEXT, nullable = False)
	
	def __repr__(self):
		return '<TransactionRecord: %r>' % (self.endpoint + ' ' + self.response + ' ' + self.timestamp)	
		
class ErrorRecord(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	endpoint = db.Column(db.String(255), nullable=False)
	timestamp = db.Column(db.DATETIME, nullable=False)
	error_message = db.Column(db.String(120), nullable=False)
	status = db.Column(db.Integer, nullable=False)	
	xml_body = db.Column(db.TEXT, nullable = False)
	
	def __repr__(self):
		return '<TransactionRecord: %r>' % (self.endpoint + ' ' + self.response + ' ' + self.timestamp)	
		
		
def log_transaction(endpoint, timestamp, status, xml_body):
	transaction = TransactionRecord(endpoint=endpoint, timestamp=timestamp, status=status, xml_body=xml_body)
	db.session.add(transaction)
	db.session.commit()
	db.session.close()	
	
		
def log_error(endpoint, timestamp, error_message, status, xml_body):
	error = ErrorRecord(endpoint=endpoint, timestamp=timestamp, error_message=error_message, status=status, xml_body=xml_body)
	db.session.add(error)
	db.session.commit()
	db.session.close()	
	
def db_test():
	#db.create_all()
	return("Done.")
	#return str(db.session.execute('select * from upload_record where id=10').fetchone())