from os import environ, path
from dotenv import load_dotenv

#just returns URL of config.py then uses that to get the Current Directory 
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
print(basedir)

class Config:
    """Set Flask configuration vars from .env file."""
    # General Config
    #SECRET_KEY = environ.get('SECRET_KEY')
    #FLASK_APP = environ.get('FLASK_APP')
    #FLASK_ENV = environ.get('FLASK_ENV')
    # Static Assets
    STATIC_FOLDER = environ.get('STATIC_FOLDER')
    TEMPLATES_FOLDER = environ.get('TEMPLATES_FOLDER')