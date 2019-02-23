import os 

# PYTHONUNBUFFERED=1;SECRET_KEY=12312321;SQLALCHEMY_DATABASE_URI=sqlite:///site.db

class Config:
	#SECRET_KEY = os.environ.get('SECRET_KEY')
	SECRET_KEY = '12312321'
	#SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	SQLALCHEMY_DATABASE_URI ='sqlite:///site.db'
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True 
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')