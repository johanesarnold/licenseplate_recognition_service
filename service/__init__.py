import os, logging, datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app                                   = Flask(__name__)
app.config.from_pyfile('../config.py')
basedir                               = os.path.abspath(os.path.dirname(__file__))
db                                    = SQLAlchemy(app)

logTime      = '[' + datetime.datetime.now().strftime("%a %Y-%m-%d %H:%M:%S") + ']'
LOG_FILENAME = basedir+'/log/flask.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)

from service.models import *
from service.controllers import *

app.register_blueprint(routes.bp, url_prefix="/api")
