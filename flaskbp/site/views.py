import traceback
from flask import current_app, url_for, render_template, redirect, flash, \
    request, jsonify
from flask_security import current_user
from . import site


@site.route('/')
def site_root():
    return redirect(url_for('site.hello'))


@site.route('/hello')
def hello():
    if current_user.is_authenticated:
        name = current_user.first_name
        payload = "Hello {}!".format(name)
    else:
        payload = "Hello World!"
    return render_template('hello.html', payload=payload)


@site.route('/status')
def status():
    status = 'healthy'
    return jsonify(status=status)


@site.after_request
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


@site.errorhandler(Exception)
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
