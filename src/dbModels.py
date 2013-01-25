from google.appengine.ext import db 	# For using google's datastore (database)

# Database class for storing entries
class Entry(db.Model):
	title = db.StringProperty(required=True)
	description = db.StringProperty(required=True,multiline=True)
	location = db.StringProperty(required=True,default="Boston")
	author = db.StringProperty(required=True,default="Arthur")
	created_on = db.DateTimeProperty(auto_now_add=True)
	accomplished_on = db.StringProperty
	is_accomplished = db.BooleanProperty(default=False)