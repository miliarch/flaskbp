import traceback
from flask import current_app, url_for, render_template, redirect, flash, \
    request, jsonify
from flask_security import login_required, current_user
from . import admin


@admin.route('/')
def admin_redir():
    return redirect(url_for('admin.manage_db'))


@admin.route('/dbman')
@login_required
def manage_db():
    return render_template('manage_db.html')


@admin.route('/raze_database', methods=['POST'])
@login_required
def raze_db():
    from .init_test_db import refresh_db
    refresh_db()
    msg = u'DB RAZED!'
    flash(msg, 'success')
    return redirect(url_for('admin.manage_db'))


@admin.after_request
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
        current_app.logger.info(log_str)
    return response


@admin.errorhandler(Exception)
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
    current_app.logger.error(log_str)
    return etype, 500
