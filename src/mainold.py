from google.appengine.ext import db 	# For using google's datastore (database)
from dbModels import Entry
import webapp2 							# Required for use with google app engine
from handler import CustomHandler 		# For cleaner page rendering
import uuid								# For easy unique ID generation
from google.appengine.api import users	# Google Account Authorization for an Easy and 
										# Secure Authorization System
from authorization import Authorization	# Check User Permission(s)
from webapp2_extras.routes import RedirectRoute

from submission import SubmitEntryPage

# Main (starting) page handler class
class MainPage(CustomHandler):
	def get(self):
  		#self.response.headers['Content-Type'] = 'text/html'
  		user = users.get_current_user()
  		if not user or user.email() not in ["Arthur.Safira@gmail.com", "Anarkia@gmail.com"]:
  			error = "P.S. You must be Nicole or Arthur to access the site."
  			if user:
  				sign_out_url = users.create_logout_url("/")
				self.render('index.html', error = error, url = sign_out_url)
			else:
				sign_in_url = users.create_login_url("/")
				self.render('index.html', error = error, url = sign_in_url)
		else:
			self.render('index.html', url="/todo")

"""
# To-Be Authorization page Handler
class QuizPage(CustomHandler):
	def get(self):
		user = users.get_current_user()
		check_authorization = Authorization()
		if not (user):
			error = "You must sign in!"
			sign_in_url = users.create_login_url("/")
			self.render('sorry.html', user = 'Someone', error=error, url=sign_in_url)
		elif user and check_authorization.is_not_authorized(user.email()):
			error = "Please ask Nicole or Arthur for access =D"
			sign_out_url = users.create_logout_url("/")
			self.render('sorry.html', user = user.nickname, error=error, url=sign_out_url)
		
		else:	
			if user:
				greeting = ("Welcome, %s! sign out" % user.nickname())
				link = users.create_logout_url("/")
			else:
				greeting = "Sign in or register"
				link = users.create_login_url("/")
			self.render('quiz_page.html',greeting=greeting, link=link, error='')

	def post(self):
		user = users.get_current_user()
		if self.request.get('answer') == "Nicole":
			self.redirect("/nicole")
		elif self.request.get('answer') == "Arthur":
			self.redirect("/arthur")
		else:
			error = 'Please select at least one option, %s!' % user.nickname()
			self.render('quiz_page.html',greeting='',error=error)
"""

# Landing page handler for Nicole
class NicolePage(CustomHandler):
  def get(self):
    self.render('nicole.html')

# Landing page handler for Arthur
class ArthurPage(CustomHandler):
  def get(self):
    self.render('arthur.html')

"""
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
"""

# Full list of entries handler
class ListPage(CustomHandler, Authorization):
	def get(self):	
		if self.user_is_authorized():
			# Find all entries and show them on a page
			entries = db.GqlQuery("SELECT * FROM Entry ORDER BY created_on DESC")
			self.render('list_page.html',entries=entries)

# Single entry View handler
class ViewEntryPage(CustomHandler, Authorization):
	def get(self, id):
		if self.user_is_authorized():
			# Find the entry with the specific id and render it on a page alone.
			entry = db.GqlQuery("SELECT * FROM Entry WHERE id = '%s' " % id)
			self.render('single_entry_page.html', entry=entry[0])
		
class NotAllowedInPage(CustomHandler):
	def get(self, id):
		user = users.get_current_user()
		self.render('sorry.html', user = user.nickname)

# URI mapping for app engine
app = webapp2.WSGIApplication([('/',MainPage),('/nicole',NicolePage),('/arthur',ArthurPage),
				RedirectRoute('/todo',ListPage,'view-all-entries',strict_slash=True),
				('/todo/new',SubmitEntryPage), (r'/todo/(.*)', ViewEntryPage)],
				debug=True)
 
