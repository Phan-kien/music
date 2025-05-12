from flask import Blueprint, request, jsonify, session, Flask
from dao.daomanager import DAOManager
from config.db import get_connection


dao_manager = DAOManager(get_connection())
app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    try:
        # Lấy dữ liệu từ request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Lấy DAO User thông qua DAOManager
        user_dao = dao_manager.get_user_dao()
        
        # Xác thực người dùng
        user = user_dao.verify_user_credentials(username, password)
        
        if user:
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'message': str(e)}), 500
@app.route('/api/logout', methods=['POST'])
def logout():
    try:
        # Xóa session của người dùng
        session.clear()  # Xóa tất cả dữ liệu trong session

        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/profile', methods=['GET'])
def profile():
    if 'user_id' not in session:
        return jsonify({'message': 'Please log in first'}), 401

    # Truy xuất thông tin người dùng từ session
    user_id = session['user_id']
    username = session['username']
    email = session['email']

    return jsonify({
        'user_id': user_id,
        'username': username,
        'email': email
    }), 200
