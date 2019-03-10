from flask import url_for, render_template, redirect, flash, request, Markup, \
    jsonify
from flask_security import login_required, current_user
from slugify import slugify
from flaskbp import app, user_datastore, security, db_session, logger
from .models import Role, User


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def site_root(path):
    """ Catch all path, credit to Oli -http://flask.pocoo.org/snippets/57/ """
    log_str = 'redirect on catch-all path'
    logger.info(log_str)
    return redirect(url_for('hello'))


@app.route('/hello')
def hello():
    log_str = 'hello world!'
    logger.debug(log_str)
    if current_user.is_authenticated:
        name = current_user.first_name
        payload = "Hello {}!".format(name)
    else:
        payload = "Hello World!"
    return render_template('hello.html', payload=payload)


@login_required
@app.route('/admin')
@login_required
def admin():
    return redirect(url_for('admin_manage_db'))


@login_required
@app.route('/admin/dbman')
@login_required
def admin_manage_db():
    return render_template('admin_manage_db.html')


@login_required
@app.route('/admin/raze_database', methods=['POST'])
@login_required
def admin_raze_db():
    from .init_test_db import refresh_db
    refresh_db()
    msg = u'DB RAZED!'
    flash(msg, 'success')
    return redirect(url_for('admin_manage_db'))
