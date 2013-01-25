from google.appengine.ext import db 	# For using google's datastore (database)
from dbModels import Entry
import webapp2 							# Required for use with google app engine
from handler import CustomHandler 		# For cleaner page rendering
import uuid								# For easy unique ID generation
from google.appengine.api import users	# Google Account Authorization for an Easy and 
										# Secure Authorization System
from authorization import Authorization	# Check User Permission(s)
from webapp2_extras.routes import RedirectRoute

# New entry page handler
class SubmitEntryPage(CustomHandler, Authorization):

	# Without POST information, load regular page
	def get(self):
		if self.user_is_authorized():
			self.render('new_entry.html',error='')

	def post(self):
		if self.user_is_authorized():
		
			# Should receive title and entry (description) as headers in POST
  			title = self.request.get("title")
			description = self.request.get("description")
			location = self.request.get("location")
		
			# If they are valid, create a unique ID for the post, save it to the database,
			# and load the entry alone on a formatted page
			if title and description and location:
				id = str(uuid.uuid1())
				new_entry = Entry(title=title, description=description, location=location, id=id)
				new_entry.put()
			
				self.redirect("/todo/" + id)
		
			# Otherwise, return to page and report an error to the user
			else:
				self.render('new_entry.html',error='Please fill in all fields!!')