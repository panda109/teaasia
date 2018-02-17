# wsgi.py

#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Catalog
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from flask_uploads import configure_uploads, patch_request_class
from app import images
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

configure_uploads(app, images)
patch_request_class(app)

# server = Server(host="0.0.0.0", port=5000 , debug = True, ssl_context=context)
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Catalog=Catalog)

if __name__ == '__main__':
    app.run()