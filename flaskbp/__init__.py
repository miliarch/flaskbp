import logging
from flask import Flask
from flask_security import Security, SQLAlchemySessionUserDatastore
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.contrib.fixers import ProxyFix
from .admin import admin
from .site import site

# Create application
app = Flask(__name__)
app.config.from_object('config')
app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)

# Register blueprints
app.register_blueprint(site, url_prefix='/')
app.register_blueprint(admin, url_prefix='/admin')

# Configure logging
logfile = '{ld}/{ln}.log'.format(
    ld=app.config['LOG_DIR'],
    ln=__name__)

# Create file handler
fh = logging.FileHandler(logfile)
fh.setLevel(logging.DEBUG)

# Create formatter
fmt_str = '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt_str)

# Add formatter to file handler
fh.setFormatter(formatter)

# Add file handler to logger
app.logger.addHandler(fh)

# Log application startup
log_str = '{} starting'.format(__name__)
app.logger.info(log_str)

# Configure and connect database
log_str = 'Connecting to database: '
log_str += '{}'.format(app.config['SQLALCHEMY_DATABASE_URI'])
app.logger.info(log_str)

db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                          convert_unicode=True)

Base = declarative_base()

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=db_engine))

Base.query = db_session.query_property()

# Configure Flask-Security
from .models import Role, User  # This import must happen after Base is defined
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

# Check if database refresh is necessary
if app.config['DEBUG'] and app.config['RESET_DB']:
    from .admin.init_test_db import refresh_db
    log_str = 'DEBUG and RESET_DB config values are True, refreshing db'
    app.logger.info(log_str)
    refresh_db()

# Record successful setup
app.logger.info('App setup complete')
