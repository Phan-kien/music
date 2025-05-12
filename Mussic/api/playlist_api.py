from flask import Blueprint, request, jsonify
from dao.daomanager import DAOManager
from config.db import get_connection

playlist_api = Blueprint('playlist_api', __name__)
dao_manager = DAOManager(get_connection())

@playlist_api.route('/api/playlists', methods=['POST'])
def create_playlist():
    try:
        data = request.get_json()
        user_id = data['user_id']
        playlist_name = data['playlist_name']

        # Lấy DAO Playlist thông qua DAOManager
        playlist_dao = dao_manager.get_playlist_dao()

        # Tạo playlist
        playlist = playlist_dao.create_playlist(user_id, playlist_name)

        return jsonify(playlist.to_dict()), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500