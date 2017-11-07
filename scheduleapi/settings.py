import tempfile
import os
db_file = tempfile.NamedTemporaryFile()


class Config(object):
    SECRET_KEY = 'secret key'


class ProdConfig(Config):
    ENV = 'prod'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'

    CACHE_TYPE = 'simple'


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    MONGODB_SETTINGS = {
            "db": "Scheduletest",
            "host": os.environ['DB_PORT_27017_TCP_ADDR'],
            "port": 27017
            }

    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = "saly"


class TestConfig(Config):
    ENV = 'test'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_file.name
    SQLALCHEMY_ECHO = True

    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False
