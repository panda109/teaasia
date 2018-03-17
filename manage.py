# manage.py

#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Catalog, Story, Car_type, Tour_type
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from flask_uploads import configure_uploads, patch_request_class
from app import images
from werkzeug.security import generate_password_hash
from sqlalchemy.orm.dynamic import CollectionHistory
#from flask_uploads import UploadSet, IMAGES
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
#images = UploadSet('images', IMAGES)

configure_uploads(app, images)
patch_request_class(app)

manager = Manager(app)
migrate = Migrate(app, db)


# server = Server(host="0.0.0.0", port=5000 , debug = True, ssl_context=context)
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Catalog=Catalog)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command("http", Server(host="0.0.0.0", use_debugger=True, port=5000, use_reloader=True))
manager.add_command("https", Server(host="0.0.0.0", port=8100, ssl_crt='openssl/server.crt', ssl_key='openssl/server.key'))
# manager.add_command("https", Server(host="0.0.0.0",use_debugger=True,port = 443, use_reloader=True, ssl_context='adhoc'))


@manager.command
def rebuild():
    db.drop_all()
    db.create_all()
    db.session.commit()
    db.session.add(Role(name='Admin'))
    db.session.add(Role(name='User'))
    db.session.add(Role(name='Provider'))
    db.session.add(Catalog(catalog_name="Tea package"))
    db.session.add(Catalog(catalog_name="Tea set"))
    db.session.add(Catalog(catalog_name="Tea food"))
    db.session.commit()

@manager.command
def story():
    story1 = Story(title = 'Elephone1', imgurl = 'elephone1.jpg',location = 'AAA', description = 'daassdfsdfkjfksljfklsjfljsdlfjsd', author = 'Tim',hitnumber = 0 , available = True)
    story2 = Story(title = 'Montain1', imgurl = 'images_11.jpg',location= 'BBB', description = 'dsfdfdaaskjfksljfklsjfljsdlfjsd', author = 'Grace' ,hitnumber = 0 , available = True)
    story3 = Story(title = 'Sea1', imgurl = 'images1.jpg',location = 'CCC', description = '13232daaskjfksljfklsjfljsdlfjsd', author = 'Tony',hitnumber = 3 , available = True)
    story4 = Story(title = 'Sea2', imgurl = 'images2.jpg',location = 'CCC', description = '13232daaskjfksljfklsjfljsdlfjsd', author = 'Tony',hitnumber = 2 , available = True)
    story5 = Story(title = 'Sea3', imgurl = 'images3.jpg',location = 'CCC', description = '13232daaskjfksljfklsjfljsdlfjsd', author = 'Tony',hitnumber = 1 , available = True)
    db.session.add(story1)
    db.session.add(story2)
    db.session.add(story3)
    db.session.add(story4)
    db.session.add(story5)
    db.session.commit()

@manager.command
def admin():
    user = User()
    user.username = 'Tim'
    user.role_id = 1
    user.email = 'yr6703@yahoo.com.tw'
    user.phone = '0921111111'
    user.add = 'sdfdsfsdfsdfsd'
    user.password_hash = generate_password_hash('1111', method="pbkdf2:sha1")
    user.is_admin = True
    user.confirmed = True
    db.session.add(user)
    db.session.commit()

@manager.command
def user():
    user = User()
    user.username = 'test'
    user.role_id = 2
    user.email = 'test@test.com'
    user.phone = '0921111111'
    user.add = 'sfsfsdfsafsdfsfasfsfa'
    user.password_hash = generate_password_hash('1111', method="pbkdf2:sha1")
    user.is_admin = False
    user.confirmed = True
    db.session.add(user)
    db.session.commit()   

@manager.command
def car():
    car1 = Car_type()
    car1.car_name = 'Wish, Previa(4 pax)'
    car1.value = 1
    car2 = Car_type()
    car2.car_name = 'Wish, Previa(6 pax)'
    car2.value = 2
    car3 = Car_type()
    car3.car_name = 'Wolks vagon(8 pax)'
    car3.value = 3
    car4 = Car_type()
    car4.car_name = 'Benz Vito(8 pax)'
    car4.value = 4
    db.session.add(car1)
    db.session.add(car2)
    db.session.add(car3)
    db.session.add(car4)
    db.session.commit()   
#[("1",'Wish, Previa(5 people)'), ("2",'Wish, Previa(7 people)'), ("3",'Wolks vagon(9 people)'), ("4",'Benz Vito(9 people)')])
@manager.command
def tour():
    tour1 = Tour_type()
    tour1.tour_name = '8 hours'
    tour1.value = 1
    tour2 = Tour_type()
    tour2.tour_name = '10 hours'
    tour2.value = 2
    tour3 = Tour_type()
    tour3.tour_name = '2 days'
    tour3.value = 3
    tour4 = Tour_type()
    tour4.tour_name = '3 days'
    tour4.value = 4
    tour5 = Tour_type()
    tour5.tour_name = '4 days'
    tour5.value = 5
    tour6 = Tour_type()
    tour6.tour_name = '5 days'
    tour6.value = 6
    tour7 = Tour_type()
    tour7.tour_name = '6 days'
    tour7.value = 7
    tour8 = Tour_type()
    tour8.tour_name = '7 days'
    tour8.value = 8
    db.session.add(tour1)
    db.session.add(tour2)
    db.session.add(tour3)
    db.session.add(tour4)
    db.session.add(tour5)
    db.session.add(tour6)
    db.session.add(tour7)
    db.session.add(tour8)
    db.session.commit()   
#[("1",'8 hours'), ("2",'10 hours'), ("3",'2 days'), ("4",'3 days'), ("5",'4 days'), ("6",'5 days'), ("7",'6 days'), ("8",'7 days')]
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
