from google.appengine.api import users

class Authorization():
	def user_is_authorized(self):
	
		user = users.get_current_user()
		authorized_emails = ('anarkia@gmail.com', 'Arthur.Safira@gmail.com')
		
		if not (user):
			error = "you must sign in!"
			sign_in_url = users.create_login_url("/")
			self.render('sorry.html', user = 'Someone', error=error, url=sign_in_url)
			return False
			
		elif user.email() not in authorized_emails:
			error = "ask Nicole or Arthur for access."
			sign_out_url = users.create_logout_url("/")
			self.render('sorry.html', user = user.nickname, error=error, url=sign_out_url)
			return False
		
		return True