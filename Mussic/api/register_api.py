from flask import Blueprint, request, jsonify
from dao.daomanager import DAOManager
from config.db import get_connection

register_api = Blueprint('register_api', __name__)
dao_manager = DAOManager(get_connection())
user_dao = dao_manager.get_user_dao()

@register_api.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if user_dao.get_user_by_email(email):
        return jsonify({'success': False, 'message': 'Email đã tồn tại.'})

    user_dao.create_user(username, email, password)
    return jsonify({'success': True, 'message': 'Đăng ký thành công.'})