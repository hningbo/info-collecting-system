from flask import Blueprint, send_file
from flask import request, session, render_template, escape, current_app, redirect
from io import BytesIO
from urllib.parse import quote
import service.info_service as info_service
import service.user_service as user_service
import xlwt

bp = Blueprint('info', __name__, url_prefix='/info')


@bp.route('/page/list')
def submit_info_page():
    if 'username' in session:
        return render_template('info_list.html', username=(session['username']), info_list=info_service.find_all_information())
    return render_template('info.html', message='尚未登录')


@bp.route('/page/submit/<string:id>', methods=['POST', 'GET'])
def submit_page(id):
    if 'username' in session:
        user = user_service.find_one_user_by_name(session['username'])
        realname = user['realname']
        print(realname)
        info_service.delete_one_by_realname(id, realname)
        info = info_service.find_one_by_id(id)

        return render_template('info_submit.html', length=range(len(info['content'])-1), info=info)
    return redirect('/')


@bp.route('/page/subscribe')
def subscribe_info_page():
    if 'username' in session:
        return render_template('info_subscribe.html', username=session['username'])
    return render_template('info.html', message='尚未登录')


@bp.route('/subscribe', methods=['GET', 'POST'])
def subscribe_info():
    if 'username' in session:
        if request.method == 'POST':
            print(request.form)
            name = request.form['info_name']
            subscriber = user_service.find_one_user_by_name(session['username'])['realname']
            end_time = request.form['end_time'].replace('T', ' ')
            number = request.form['number']
            content = []
            for i in range(int((len(request.form)-3)/3)+1):
                if i == 0:
                    continue
                content.append({'name': request.form['item_name'+str(i)], 'demo': request.form['item_demo'+str(i)], 'request': request.form['item_request'+str(i)]})
            info_service.add_information(name, subscriber, end_time, number, content)
            return render_template('info.html', message='成功发布任务')
    return redirect('/')


@bp.route('/<string:id>/submit', methods=['GET', 'POST'])
def submit_info(id):
    if 'username' in session:
        username = session['username']
        user = user_service.find_one_user_by_name(username)
        kv = [('姓名', user['realname'])]
        info = dict(request.form)
        for key in info:
            kv.append((key, info[key]))
        info_service.add_one_to_collection(id, dict(kv))
        info = info_service.find_one_by_id(id)
        return render_template('info.html', message='成功提交')
    return redirect('/')


@bp.route('/delete/<string:id>')
def delete_info(id):
    if session['username'] == 'admin':
        info_service.delete_one_by_id(id)
        return redirect('/admin')


@bp.route('/download/<string:id>', methods=['GET'])
def download_info(id):
    #info = []
    #for i in info_service.find_by_collection(id):
        #info.append(i)
    if session['username'] == 'admin':
            path = './static/'
            info = info_service.find_one_by_id(id)
            if not info:
                return render_template('info.html', message='信息表不存在！')
            infoname = info['infoname']
            file_name = infoname+'.xlsx'
            infos = info_service.find_by_collection(id)
            infos = [i for i in infos]
            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('My Worksheet')
            if infos:
                for info in infos:
                    info.pop('_id')
                keys = [i.keys() for i in infos]
                keys = keys[0]
                print(infos)
                for i, key in enumerate(keys):
                    worksheet.write(0, i, key)
                for i, info in enumerate(infos, 0):
                    for j, key in enumerate(keys):
                        worksheet.write(i+1, j, info.setdefault(key, ''))
            workbook.save(''.join([path, file_name]))

            return redirect('./static/'+file_name)
    else:
        return redirect('info.html', message='权限不足！请联系管理员！')

