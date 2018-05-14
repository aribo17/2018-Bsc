# Statement for enabling the development environment
DEBUG = True

# import engine and sessionmaker
from sqlalchemy import create_engine
#from sqlalchemy_utils import database_exists, create_database

# Define the application directory
import os
#from dotenv import load_dotenv
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#load_dotenv(os.path.join(BASE_DIR, '.pipenv'))


# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}


# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
