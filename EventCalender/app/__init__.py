# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
#from config import engine
from sqlalchemy.orm import sessionmaker, scoped_session
# declarative extension in SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
#from app.mod_auth.models import MyJSONEncoder

#from flask_migrate import Migrate
#from config import Config
#migrate = Migrate()


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')


# Define the database object which is imported
# by modules and controllers
# db = SQLAlchemy(app)
db = SQLAlchemy(app)


Bootstrap(app)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_auth.controllers import mod as mod_module
from app.mod_auth.models import MyJSONEncoder

app.json_encoder = MyJSONEncoder

# Register blueprint(s
app.register_blueprint(auth_module)
app.register_blueprint(mod_module)
# app.register_blueprint(xyz_module)
# ..


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


# Build the database:
# This will create the database file using SQLAlchemy

db.create_all()
