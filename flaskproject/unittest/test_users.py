import unittest
from flaskproject import create_app, db, mail


app = create_app()
app.app_context().push()

TEST_DB = 'site.db'


class BasicTests(unittest.TestCase):

	############################
	#### setup and teardown ####
	############################

	# executed prior to each test
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False
		app.config['SECRET_KEY'] = '213123asd'
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +  TEST_DB
		self.app = app.test_client()
		db.drop_all()
		db.create_all()

		# Disable sending emails during unit testing
		mail.init_app(app)
		self.assertEqual(app.debug, False)

	# executed after each test
	def tearDown(self):
		pass

	###############
	#### utils ####
	###############

	def register(self, user, email, password, confirm):
		return self.app.post(
			'/register',
			data=dict(username = user, email=email, password=password, confirm_password=confirm),
			follow_redirects=True
		)

	def login(self, email, password):
		return self.app.post(
			'/login',
			data=dict(email=email, password=password),
			follow_redirects=True
		)

	def logout_user(self):
		return self.app.get(
			'/logout',
			follow_redirects=True
		)

	###############
	#### tests ####
	###############

	def test_main_page(self):
		response = self.app.get('/', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_valid_user_registration(self):
		response = self.register('patKen', 'patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Your account has been created. You are now able to log in', response.data)

	def test_invalid_user_registration_different_passwords(self):
		response = self.register('patKen', 'patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsNotAwesome')
		self.assertIn(b'Field must be equal to password.', response.data)

	def test_invalid_user_registration_duplicate_email(self):
		response = self.register('patKen', 'patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
		self.assertEqual(response.status_code, 200)
		response = self.register('patKen', 'patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
		self.assertIn(b'That email is taken. Please choose a different one.', response.data)


if __name__ == "__main__":
	unittest.main()




