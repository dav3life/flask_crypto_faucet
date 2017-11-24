from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flaskext.mysql import MySQL
 
mysql = MySQL()
# If you get an error on the next line on Python 3.4.0, change to: Flask('app')
# where app matches the name of this file without the .py extension.
app = Flask(__name__)
app.config['CSRF_ENABLED'] = True

## use this config to get it running locally for testing purposes but can also work on a vps 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_template.db'

## use this config for running a mysql database 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://msqlusername:mysqlpassword@localhost/mysqldatabasename'
app.config['SECRET_KEY'] ='you will never guess it !'
app.config['RECAPTCHA_PUBLIC_KEY'] ='your google recaptcha public key '
app.config['RECAPTCHA_PRIVATE_KEY'] ='your google recaptcha private key '
app.config['TESTING'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from routes import *
from models import *

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app

if __name__ == '__main__':
	app.run()
