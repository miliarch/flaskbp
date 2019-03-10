import traceback
from datetime import datetime
from flask import url_for, render_template, redirect, flash, request, Markup, \
    jsonify
from flask_security import login_required, current_user
from slugify import slugify
from flaskbp import app, user_datastore, security, db_session
from .models import Role, User

app.logger.info('views loaded')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def site_root(path):
    """ Catch all path, credit to Oli -http://flask.pocoo.org/snippets/57/ """
    return redirect(url_for('hello'))


@app.route('/hello')
def hello():
    if current_user.is_authenticated:
        name = current_user.first_name
        payload = "Hello {}!".format(name)
    else:
        payload = "Hello World!"
    return render_template('hello.html', payload=payload)


@app.route('/status')
def status():
    status = 'healthy'
    return jsonify(status=status)


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


@app.after_request
def after_request(response):
    fp = request.full_path
    fp = fp[:-1] if fp[-1] == '?' else fp
    if int(response.status_code / 100) != 5:
        log_str = '{ra} {m} {s} {fp} {stat}'.format(
            ra=request.remote_addr,
            m=request.method,
            s=request.scheme,
            fp=fp,
            stat=response.status)
        app.logger.info(log_str)
    return response


@app.errorhandler(Exception)
def exceptions(e):
    etype = 'INTERNAL SERVER ERROR'
    fp = request.full_path
    fp = fp[:-1] if fp[-1] == '?' else fp
    tb = traceback.format_exc()
    log_str = '{ra} {m} {s} {fp} {stat} {tb}'.format(
        ra=request.remote_addr,
        m=request.method,
        s=request.scheme,
        fp=fp,
        stat='500 {}'.format(etype),
        tb=tb)
    app.logger.error(log_str)
    return etype, 500
