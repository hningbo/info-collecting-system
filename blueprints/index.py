from flask import Blueprint
from flask import render_template, session, current_app, redirect
import service.info_service as info_service

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    if 'username' in session:
        if session['username'] == 'admin':
            return redirect('/admin')
        return redirect('/info/page/list')
    return render_template('index.html')


@bp.route('/admin')
def admin():
    infos = info_service.find_all_information()
    if 'username' in session:
        if session['username'] == 'admin':
            return render_template('admin.html', infos=infos)

    return redirect('/')


@bp.route('/is')
def info_system():
    if 'username' in session:
        return render_template('homework_list.html', username=session['usernmae'])
    return render_template('index.html')