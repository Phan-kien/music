from flask import Blueprint, request, jsonify
from dao.daomanager import DAOManager
from config.db import get_connection

like_api = Blueprint('like_api', __name__)
dao_manager = DAOManager(get_connection())
like_dao = dao_manager.get_like_dao()
# API thích bài hát
@like_api.route('/api/like', methods=['POST'])
def like_song():
    data = request.get_json()
    user_id = data.get('user_id')
    song_id = data.get('song_id')

    if not all([user_id, song_id]):
        return jsonify({'success': False, 'message': 'Thiếu user_id hoặc song_id'}), 400

    success = like_dao.like_song(user_id, song_id)

    if not success:
        return jsonify({'success': False, 'message': 'Bài hát đã được yêu thích trước đó'}), 409

    return jsonify({'success': True, 'message': 'Đã thêm bài hát vào danh sách yêu thích'})

# API bỏ thích bài hát
@like_api.route('/api/unlike', methods=['POST'])
def unlike_song():
    data = request.get_json()
    user_id = data.get('user_id')
    song_id = data.get('song_id')

    if not all([user_id, song_id]):
        return jsonify({'success': False, 'message': 'Thiếu user_id hoặc song_id'}), 400

    success = like_dao.unlike_song(user_id, song_id)

    if not success:
        return jsonify({'success': False, 'message': 'Bài hát chưa được yêu thích'}), 404

    return jsonify({'success': True, 'message': 'Đã xóa bài hát khỏi danh sách yêu thích'})

# API lấy danh sách bài hát yêu thích của người dùng
@like_api.route('/api/liked-songs/<int:user_id>', methods=['GET'])
def get_liked_songs(user_id):
    songs = like_dao.get_liked_songs_by_user(user_id)
    if not songs:
        return jsonify({'success': False, 'message': 'Không có bài hát yêu thích.'}), 404
    return jsonify({'success': True, 'songs': songs})
