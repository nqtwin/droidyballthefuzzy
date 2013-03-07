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
class MainPage(CustomHandler, Authorization):
	def get(self):
  		#self.response.headers['Content-Type'] = 'text/html'
  		user = users.get_current_user()
  		if self.user_is_authorized():
  			self.render('index.html', url = "/todo")

  		"""if not user or user.email() not in ["Arthur.Safira@gmail.com", "Anarkia@gmail.com"]:
  			error = "You must be Nicole or Arthur to access the site."
  			if user:
  				sign_out_url = users.create_logout_url("/")
				self.render('index.html', error = error, url = sign_out_url)
			else:
				sign_in_url = users.create_login_url("/")
				self.render('index.html', error = error, url = sign_in_url)
		else:
			self.render('index.html', url="/todo") """

# Landing page handler for Nicole
class NicolePage(CustomHandler):
  def get(self):
    self.render('nicole.html')

# Landing page handler for Arthur
class ArthurPage(CustomHandler):
  def get(self):
    self.render('arthur.html')

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
			entry = Entry.get_by_key_name(id)
			if entry:
				self.render('single_entry_page.html', entry=entry, id=id)
	
	def post(self, id):
		date_accomplished = self.request.get("date")
		entry = Entry.get_by_key_name(id)
		entry.accomplished_on = date_accomplished
		entry.is_accomplished = True
		db.put(entry)
		self.render('single_entry_page.html', entry=entry, id=id)
		
class NotAllowedInPage(CustomHandler):
	def get(self, id):
		user = users.get_current_user()
		self.render('sorry.html', user = user.nickname)

# URI mapping for app engine
app = webapp2.WSGIApplication([('/',MainPage),('/nicole',NicolePage),('/arthur',ArthurPage),
				RedirectRoute('/todo',ListPage,'view-all-entries',strict_slash=True),
				('/todo/new',SubmitEntryPage), (r'/todo/(.*)', ViewEntryPage)],
				debug=True)
 
