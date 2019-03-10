#!/usr/bin/env python3
from flask_security.utils import encrypt_password
from flaskbp import app, db_engine, db_session, user_datastore, Base, logger


def create_test_admin_user():
    with app.app_context():
        log_str = 'creating admin user'
        logger.debug(log_str)
        user_datastore.create_user(
            email=app.config['TEST_ADMIN_EMAIL'],
            username=app.config['TEST_ADMIN_USER'],
            password=encrypt_password(app.config['TEST_ADMIN_PASS']),
            first_name=app.config['TEST_ADMIN_FIRST_NAME'],
            last_name=app.config['TEST_ADMIN_LAST_NAME'])
        db_session.commit()


def destroy_db():
    log_str = "destroying database"
    logger.debug(log_str)
    with app.app_context():
        logger.debug(type(db_engine))
        Base.metadata.drop_all(bind=db_engine)


def init_db():
    log_str = "initializing database"
    logger.debug(log_str)
    with app.app_context():
        Base.metadata.create_all(bind=db_engine)


def refresh_db():
    log_str = "running refresh routine"
    logger.debug(log_str)
    destroy_db()
    init_db()
    create_test_admin_user()


if __name__ == '__main__':
    refresh_db()
