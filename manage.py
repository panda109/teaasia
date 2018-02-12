# manage.py

#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Catalog
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

images = UploadSet('images', IMAGES)
configure_uploads(app, images)
patch_request_class(app)

manager = Manager(app)
migrate = Migrate(app, db)
#server = Server(host="0.0.0.0", port=5000 , debug = True, ssl_context=context)
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
#manager.add_command("runserver", app.run(host="0.0.0.0", port=5000 , debug = True))
#manager.add_command("server", app.run(host="0.0.0.0", port=443 , debug = True, ssl_context='adhoc'))

@manager.command
def rebuild():
    db.drop_all()
    db.create_all()
    db.session.commit()
    db.session.add(Role(name = 'Admin'))
    db.session.add(Role(name = 'User'))
    db.session.add(Role(name = 'Provider'))
    db.session.add(Catalog(catalog_name = "Tea"))
    db.session.add(Catalog(catalog_name = "Fruit"))
    db.session.add(Catalog(catalog_name = "Toy"))
    db.session.commit()

@manager.command
def isadmin():
    user = User.query.filter_by(id = 1).first()
    user.role_id = 1
    user.is_admin = True
    db.session.add(user)
    db.session.commit()
    
    
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
