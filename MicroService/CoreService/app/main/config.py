import os
from dotenv import load_dotenv

load_dotenv()


# uncomment the line below for postgres database url from environment variable
postgres_local_base = os.getenv('DATABASE_URL')

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.getenv('SECRET_KEY')
	DEBUG = False


class DevelopmentConfig(Config):
	DEBUG = True
	

class TestingConfig(Config):
	DEBUG = True
	TESTING = True
	# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
	# PRESERVE_CONTEXT_ON_EXCEPTION = False
	# SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
	DEBUG = False
	# uncomment the line below to use postgres
	# SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
	dev=DevelopmentConfig,
	test=TestingConfig,
	prod=ProductionConfig
)

key = Config.SECRET_KEY