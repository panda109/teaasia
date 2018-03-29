# app/models.py

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import db
from . import login_manager

class Car_type(db.Model):
    __tablename__ = 'car_type'
    id = db.Column(db.Integer, primary_key=True)
    car_name = db.Column(db.String(30))
    value = db.Column(db.Integer)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    constain = db.Column(db.String(500))
    author = db.Column(db.String(30))
    post_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'         : self.id,
           'author'     : self.author,
           'contain'    : self.constain,
           'post_datetime'  : self.post_datetime
           #'modified_at': dump_datetime(self.modified_at),
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
       }

    @classmethod
    def get_last5(cls):
        """Return list of products.

        Query the database for the first [max] products, returning each as a
        Product object
        """
        posts = Post.query.order_by(Post.id.desc()).limit(5).all()
        return posts
    
    @classmethod
    def get_all(cls):
        """Return list of products.

        Query the database for the first [max] products, returning each as a
        Product object
        """
        posts = Post.query.all()
        # print product
        return posts

    @classmethod
    def get_by_id(cls, id):
        """Query for a specific product in the database by the primary key"""
        
        post = Post.query.get(id)
        return post
    
    def __repr__(self):
        """Convenience method to show information about product in console."""
    
        return "<Item: %s>" % (self.constain)

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(10))
    total = db.Column(db.String(10))
    payment_id = db.Column(db.String(64))
    status = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(30))
    order_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    orders = db.relationship('Order_detail', backref='order', lazy='dynamic')
    shipout = db.Column(db.Boolean, default=False)
    ship_datetime = db.Column(db.String(10))

    @classmethod
    def get_all(cls):
        order = Order.query.all()
        return order
   
    def __repr__(self):
        return "<Item: %s, %s, %s>" % (self.id, self.user_id, self.order_datetime)


class Order_detail(db.Model):
    __tablename__ = 'order_detail'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(10))
    product_id = db.Column(db.String(10))
    product_name = db.Column(db.String(30))
    price = db.Column(db.String(10))
    quantity = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    @classmethod
    def get_all(cls):
        order_detail = Order_detail.query.all()
        return order_detail


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Story(db.Model):
    __tablename__ = 'story'
    id = db.Column(db.Integer, primary_key=True)
    #product_type = db.relationship("Catalog")  # -> call __repr__(self) return !!!!
    title = db.Column(db.String(30), unique=True)
    imgurl = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(500))
    location = db.Column(db.String(30), unique=False)
    author = db.Column(db.String(30), unique=False)
    hitnumber = db.Column(db.Integer)
    post_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    available = db.Column(db.Boolean, default=False)

    #catalog_id = db.Column(db.Integer, db.ForeignKey('catalog.id'))
    
    @classmethod
    def get_all(cls):
        """Return list of products.

        Query the database for the first [max] products, returning each as a
        Product object
        """
        stories = Story.query.all()
        # print product
        return stories
    
    @classmethod
    def get_top2(cls):
        stories = Story.query.order_by(Story.hitnumber.desc()).limit(2).all()
        return stories
    
    @classmethod
    def get_by_id(cls, id):
        """Query for a specific product in the database by the primary key"""
        
        story = Story.query.get(id)
        return story
    
    def __repr__(self):
        """Convenience method to show information about product in console."""
    
        return "<Item: %s>" % (self.title)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)

    
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    email = db.Column(db.String(64), unique=True, index=True)
    phone = db.Column(db.String(64))
    add = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    @classmethod
    def get_role(cls, orle_id):
        role = Role.query.filter_by(id=orle_id)
        return role

    @classmethod
    def get_all(cls):
        users = User.query.all()
        return users

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


class Catalog(db.Model):
    __tablename__ = 'catalog'
    id = db.Column(db.Integer, primary_key=True)
    catalog_name = db.Column(db.String(30))
    products = db.relationship('Product')

    @classmethod
    def get_by_id(cls, id):
        """Query for a specific catalog in the database by the primary key"""
        catalog = Catalog.query.get(id)
        return catalog
 
    @classmethod
    def get_all(cls):
        catalog = Catalog.query.all()
        return catalog
    
    def __repr__(self):
        return '{}'.format(self.catalog_name)

    
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    # product_type = db.Column(db.String(30))
    product_type = db.relationship("Catalog")  # -> call __repr__(self) return !!!!
    common_name = db.Column(db.String(30), unique=True)
    price = db.Column(db.String(10))
    imgurl = db.Column(db.String(30), unique=True)
    color = db.Column(db.String(30))
    size = db.Column(db.String(30))
    available = db.Column(db.Boolean, default=False)
    catalog_id = db.Column(db.Integer, db.ForeignKey('catalog.id'))
    
    def price_str(self):
        """Return price formatted as string $x.xx"""

        return "%s" % self.price

    def __repr__(self):
        """Convenience method to show information about product in console."""

        return "<Item: %s, %s, %s>" % (
            self.id, self.common_name, self.price_str())

    @classmethod
    def get_all(cls):
        """Return list of products.

        Query the database for the first [max] products, returning each as a
        Product object
        """
        product = Product.query.all()
        # print product
        return product
    @classmethod
    def get_last3(cls):
        product = Product.query.order_by(Product.id.desc()).limit(3).all()
        return product
    
    @classmethod
    def get_by_id(cls, id):
        """Query for a specific product in the database by the primary key"""
        
        product = Product.query.get(id)
        return product
