class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'my_precious'
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    
class DevelopmentConfig(Config):
    DEBUG = True
    # WTF_CSRF_ENABLED = False
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/tq.db'
    DEBUG_TB_ENABLED = True 

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/test_tq.db'
