#!/usr/bin/env python3
from sys import exc_info
from sqlalchemy.exc import OperationalError
from flask_security.utils import encrypt_password
from .. import app, db_engine, db_session, user_datastore, Base


def create_test_admin_user():
    with app.app_context():
        log_str = 'creating admin user'
        app.logger.info(log_str)
        user_datastore.create_user(
            email=app.config['TEST_ADMIN_EMAIL'],
            username=app.config['TEST_ADMIN_USER'],
            password=encrypt_password(app.config['TEST_ADMIN_PASS']),
            first_name=app.config['TEST_ADMIN_FIRST_NAME'],
            last_name=app.config['TEST_ADMIN_LAST_NAME'])
        db_session.commit()
        db_session.close_all()


def destroy_db():
    log_str = 'destroying database'
    app.logger.info(log_str)
    try:
        with app.app_context():
            log_str = 'closing db_session connections'
            app.logger.debug(log_str)
            db_session.close_all()
            log_str = 'dropping all tables'
            app.logger.debug(log_str)
            Base.metadata.drop_all(bind=db_engine)
    except OperationalError as err:
        log_str = 'OperationalError: {}'.format(err)
        app.logger.error(log_str)
    except:
        app.logger.debug('unexpected error: {}'.format(exc_info()[0]))


def init_db():
    log_str = "initializing database"
    app.logger.info(log_str)
    with app.app_context():
        log_str = 'creating all tables'
        app.logger.debug(log_str)
        Base.metadata.create_all(bind=db_engine)


def refresh_db():
    log_str = 'running db refresh routine'
    app.logger.info(log_str)
    destroy_db()
    init_db()
    create_test_admin_user()
    log_str = 'db refresh routine complete'
    app.logger.info(log_str)
