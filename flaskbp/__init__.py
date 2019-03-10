import logging
from flask import Flask, Markup
from flask_security import Security, SQLAlchemySessionUserDatastore
from mistune import markdown
from pathlib import Path
from pytz import timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.contrib.fixers import ProxyFix

# Create application
app = Flask(__name__)
app.config.from_object('config')
app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)

# Configure logging
logfile = '{ld}/{ln}.log'.format(
    ld=app.config['LOG_DIR'],
    ln=__name__)

# Create file handler
fh = logging.FileHandler(logfile)
fh.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter('[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')

# Add formatter to file handler
fh.setFormatter(formatter)

# Add file handler to logger
app.logger.addHandler(fh)

# Log application startup
log_str = '{} starting'.format(__name__)
app.logger.info(log_str)

# Configure and connect database
db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                          convert_unicode=True)

Base = declarative_base()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=db_engine))

Base.query = db_session.query_property()

from .models import Role, User
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

if app.config['DEBUG'] and app.config['RESET_DB']:  
    from .init_test_db import refresh_db
    log_str = 'DEBUG and RESET_DB values are True, refreshing DB'
    app.logger.debug(log_str)
    refresh_db()


def format_date_utc(dtobject, dtformat='%Y-%m-%d %H:%M:%S %Z (%z)'):
    utc = timezone('UTC')
    dtobject = utc.localize(dtobject, is_dst=None).astimezone(utc)
    return dtobject.strftime(dtformat)


def format_date_pacific(dtobject, dtformat='%A %B %-m at %-I:%M %p %Z'):
    # Credit to Ryan Greever: https://stackoverflow.com/a/34832184
    pt = timezone('US/Pacific')
    utc = timezone('UTC')
    dtobject = utc.localize(dtobject, is_dst=None).astimezone(utc)
    return dtobject.astimezone(pt).strftime(dtformat)


def parse_markdown(mdtext):
    return Markup(markdown(mdtext))

app.jinja_env.filters['format_date_utc'] = format_date_utc
app.jinja_env.filters['format_date_pacific'] = format_date_pacific
app.jinja_env.filters['parse_markdown'] = parse_markdown

from flaskbp import views
