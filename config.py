# config.py
import os
#basedir = os.path.abspath(os.path.dirname(__file__))
#UPLOADPATH = os.getcwd() + '\\static\\_upload\\images\\'
#P_IMAGEPATH = os.getcwd() + '\\static\\product\\images\\'
#S_IMAGEPATH = os.getcwd() + '\\static\\story\\images\\'

#UPLOADPATH = os.getcwd() + '/static/_upload/images/'
#P_IMAGEPATH = os.getcwd() + '/static/product/images/'
#S_IMAGEPATH = os.getcwd() + '/static/story/images/'

#IPPORT = 'bytaiwan.me'
#IPPORT = '10.90.7.37:5000'
#IPPORT = '192.168.0.18:5000'
#IPPORT = '29fa258b.ngrok.io'
mailpassword=''

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '!QIOD*Lioisfhishiwiwe98ew9233'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER_NAME = IPPORT
    SESSION_COOKIE_NAME = IPPORT
    SESSION_COOKIE_DOMAIN = IPPORT
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'bytaiwan5812@gmail.com'
    MAIL_PASSWORD = mailpassword
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[ByTaiwan]'
    FLASKY_MAIL_SENDER = 'ByTaiwan Admin <bytaiwan5812@gmail.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    UPLOADED_IMAGES_DEST = UPLOADPATH
    REDIS_URL = "redis://localhost"
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
