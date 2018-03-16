from flask import Blueprint
from flask import render_template, session, current_app, redirect
import service.info_service as info_service

bp = Blueprint('hardworking', __name__, url_prefix='/hws')


@bp.route('/')
def hws_index():
    return render_template('hardworking.html', overtimeSum=11, overtime1=1, overtime2=2, overtime3=8, u=[])


