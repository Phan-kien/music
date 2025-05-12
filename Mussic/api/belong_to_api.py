from flask import Blueprint, request, jsonify
from dao.daomanager import DAOManager
from config.db import get_connection


belong_to_api = Blueprint('belong_to_api', __name__)
dao_manager = DAOManager(get_connection())
belong_to_dao = dao_manager.get_belong_to_dao()

@belong_to_api.route('/api/playlist/add-song', methods=['POST'])
def add_song_to_playlist():
    data = request.get_json()
    playlist_id = data.get('playlist_id')
    song_id = data.get('song_id')

    if not all([playlist_id, song_id]):
        return jsonify({'success': False, 'message': 'Thiếu playlist_id hoặc song_id'}), 400

    success = belong_to_dao.add_song_to_playlist(song_id, playlist_id)

    if not success:
        return jsonify({'success': False, 'message': 'Bài hát đã có trong playlist'}), 409

    return jsonify({'success': True, 'message': 'Đã thêm bài hát vào playlist'})
