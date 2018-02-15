# config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))

UPLOADPATH = os.getcwd() + '\\static\\_uploads\\images\\'
print UPLOADPATH
IMAGEPATH = os.getcwd() + '\\static\\product\\images\\'
print IMAGEPATH
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '!QIOD*Lioisfhishiwiwe98ew9233'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #un mark SERVER_NAME {{ url_for('auth.confirm', token=token, _external=True) }}
    #SERVER_NAME = 'http://54.95.82.93:5000'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'teaasia5812@gmail.com'
    MAIL_PASSWORD = ''
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[TeaAsia]'
    FLASKY_MAIL_SENDER = 'TeaAsia Admin <tesaasia5812@gmail.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    UPLOADED_IMAGES_DEST = UPLOADPATH

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
