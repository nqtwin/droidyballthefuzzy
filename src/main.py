from google.appengine.ext import db 	# For using google's datastore (database)
import webapp2 							# Required for use with google app engine
from handler import CustomHandler 		# For cleaner page rendering
import uuid								# For easy unique ID generation
from google.appengine.api import users	# Google Account Authorization for an Easy and 
										# Secure Authorization System
#from auth import Authorization			# For cleaner user authorization checking

# Main (starting) page handler class
class MainPage(CustomHandler):
	def get(self):
  		#self.response.headers['Content-Type'] = 'text/html'
		self.render('index.html')

# To-Be Authorization page Handler
class QuizPage(CustomHandler):
	def get(self):
		user = users.get_current_user()
		check_authorization = Authorization()
		if not (user):
			error = "You must sign in!"
			sign_in_url = users.create_login_url("/")
			self.render('index.html', error=error, url=sign_in_url)
		elif user and check_authorization.is_not_authorized(user.email()):
			error = "P.S. You must be Nicole or Arthur to access the site."
			sign_out_url = users.create_logout_url("/")
			self.render('index.html', error=error, url=sign_out_url)
		
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

# Landing page handler for Nicole
class NicolePage(CustomHandler):
  def get(self):
    self.render('nicole.html')

# Landing page handler for Arthur
class ArthurPage(CustomHandler):
  def get(self):
    self.render('arthur.html')

# New entry page handler
class SubmitEntryPage(CustomHandler):

	# Without POST information, load regular page
	def get(self):
		self.render('new_entry.html',error='')

	def post(self):
		
		# Should receive title and entry (description) as headers in POST
  		title = self.request.get("title")
		description = self.request.get("description")
		
		# If they are valid, create a unique ID for the post, save it to the database,
		# and load the entry alone on a formatted page
		if title and description:
			id = str(uuid.uuid1())
			new_entry = Entry(title=title, description=description, id=id)
			new_entry.put()
			
			self.redirect("/todo/" + id)
		
		# Otherwise, return to page and report an error to the user
		else:
			self.render('new_entry.html',error='Please fill in all fields!!')

# Full list of entries handler
class ListPage(CustomHandler):
	def get(self):
		
		# Find all entries and show them on a page
		entries = db.GqlQuery("SELECT * FROM Entry ORDER BY created_on DESC")
		self.render('list_page.html',entries=entries)

# Single entry View handler
class ViewEntryPage(CustomHandler):
	def get(self, id):
	
		# Find the entry with the specific id and render it on a page alone.
		entry = db.GqlQuery("SELECT * FROM Entry WHERE id = '%s' " % id)
		self.render('list_page.html', entries = entry)

class Authorization():
	def is_not_authorized(self, email):
		authorized_emails = ('anarkia@gmail.com', 'Arthur.Safira@gmail.com')
		if email in authorized_emails:
			return False
		return True

# Database class for storing entries
class Entry(db.Model):
	title = db.StringProperty(required=True)
	description = db.StringProperty(required=True,multiline=True)
	location = db.StringProperty(required=True,default="Boston")
	author = db.StringProperty(required=True,default="Arthur")
	created_on = db.DateTimeProperty(auto_now_add=True)
	accomplished_on = db.DateTimeProperty
	is_accomplished = db.BooleanProperty(default=False)
	id = db.StringProperty(required=True)

# URI mapping for app engine
app = webapp2.WSGIApplication([('/',MainPage),('/quiz',QuizPage),('/nicole',NicolePage),('/arthur',ArthurPage),
				('/todo',ListPage),('/todo/new',SubmitEntryPage), (r'/todo/(.*)', ViewEntryPage)],
				debug=True)
 
