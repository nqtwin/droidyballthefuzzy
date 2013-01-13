import os
import webapp2
import jinja2
from jinja2 import Environment, FileSystemLoader

template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
#env = Environment(loader=PackageLoader('droidyballthefuzzy', 'templates'))
env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)

class CustomHandler(webapp2.RequestHandler):
	def render(self,template_name,**kwargs):
		self.response.write(env.get_template(template_name).render(kwargs))


