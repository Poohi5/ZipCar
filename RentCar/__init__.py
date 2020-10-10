from flask import Flask, request
import os

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_bootstrap import Bootstrap
import stripe

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
stripe_keys = {
    'secret_key': os.environ['secret_key'],
    'publishable_key': os.environ['pub_key']
        }

stripe.api_key = stripe_keys['secret_key']

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
#login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


migrate = Migrate(app, db)
manager = Manager(app)
bootstrap = Bootstrap(app)

manager.add_command('db', MigrateCommand)

from RentCar import views


