# app/models.py

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha1")

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        user = User.query.get(data.get('reset'))
        if user is None:
            return False

        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        if data.get('change_email') != self.id:
            return False

        new_email = data.get('new_email')
        if new_email is None:
            return False

        if self.query.filter_by(email=new_email).first() is not None:
            return False

        self.email = new_email
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username

class Product(db.Model):
    """An Products type.

    """
    __tablename__ = 'products'
    def __init__(self,
                 id,
                 product_type,
                 common_name,
                 price, imgurl,
                 flesh_color,
                 rind_color,
                 seedless):
        self.id = id
        self.product_type = product_type
        self.common_name = common_name
        self.price = price
        self.imgurl = imgurl
        self.flesh_color = flesh_color
        self.rind_color = rind_color
        self.seedless = bool(seedless)

    def price_str(self):
        """Return price formatted as string $x.xx"""

        return "$%.2f" % self.price

    def __repr__(self):
        """Convenience method to show information about melon in console."""

        return "<Item: %s, %s, %s>" % (
            self.id, self.common_name, self.price_str())

    @classmethod
    def get_all(cls, max=30):
        """Return list of melons.

        Query the database for the first [max] melons, returning each as a
        Melon object
        """

        cursor = db_connect()
        QUERY = """
                  SELECT id,
                         product_type,
                         common_name,
                         price,
                         imgurl,
                         flesh_color,
                         rind_color,
                         seedless
                   FROM products
                   WHERE imgurl <> ''
                   LIMIT ?;
               """

        cursor.execute(QUERY, (max,))
        product_rows = cursor.fetchall()

        # list comprehension to build a list of Melon objects by going through
        # the database records and making a melon for each row. This is done
        # by unpacking in the for-loop.

        product = [Product(*row) for row in product_rows]

        print product

        return product

    @classmethod
    def get_by_id(cls, id):
        """Query for a specific melon in the database by the primary key"""

        cursor = db_connect()
        QUERY = """
                  SELECT id,
                         product_type,
                         common_name,
                         price,
                         imgurl,
                         flesh_color,
                         rind_color,
                         seedless
                   FROM products
                   WHERE id = ?;
               """

        cursor.execute(QUERY, (id,))

        row = cursor.fetchone()

        if not row:
            return None

        product = Product(*row)

        return product