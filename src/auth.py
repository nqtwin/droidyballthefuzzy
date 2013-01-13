class Authorization:
	def is_not_authorized(self, email):
		authorized_emails = ('anarkia@gmail.com', 'Arthur.Safira@gmail.com')
		if email in authorized_emails:
			return 0
		return 1