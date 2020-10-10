'''

DB Migration Script
(Use python manage.py db migrate
python manage.py db upgrade to migrate only the changes to the DB)

Author: Pooja Patil
'''


import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from RentCar import app
from RentCar.models import db


app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
