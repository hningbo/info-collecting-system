from flask import Blueprint
from flask import render_template, request, session, escape, redirect, url_for ,current_app
import service.user_service as user_service

bp = Blueprint('user', __name__)


@bp.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        current_app.logger.debug(request.form['username'] + ' log in')
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['username'] = 'admin'
            return redirect('/admin')
        if not user_service.find_one_user_by_name(username):
            current_app.logger.debug('Fail')
            return render_template('info.html', message='用户不存在')
        else:
            if user_service.check_password(username, password) == True:
                current_app.logger.debug('Success')
                session['username'] = request.form['username']
                return redirect('/')
            else:
                return render_template('info.html', message='密码错误')
    return redirect('/')


@bp.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        print(request.form)
        username = request.form['username']
        realname = request.form['realname']
        password = request.form['password']
        if not user_service.find_one_user_by_name({'username': username}):
            user_service.add_user(username, realname, password)
            return render_template('info.html', message='成功注册')
        else:
            return render_template('info.html', message='用户已存在')
    return redirect('/')


@bp.route('/user/exit')
def user_exit():
    session.pop('username', None)
    return redirect('/')


