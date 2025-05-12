# api/song_api.py
from flask import Blueprint, jsonify, request
from dao.Song.song_dao import SongDAO
from dao.Song.Song_object import Song

song_api = Blueprint('song_api', __name__)
song_dao = SongDAO()

@song_api.route('/songs', methods=['GET'])
def get_all_songs():
    songs = song_dao.get_all_songs()
    return jsonify([vars(song) for song in songs]), 200

@song_api.route('/songs/<int:song_id>', methods=['GET'])
def get_song(song_id):
    song = song_dao.get_song_by_id(song_id)
    if song:
        return jsonify(vars(song)), 200
    return jsonify({'error': 'Song not found'}), 404

@song_api.route('/songs', methods=['POST'])
def add_song():
    data = request.get_json()
    song = Song(
        song_id=None,  # Auto-increment
        user_id=data.get('user_id'),
        song_name=data.get('song_name'),
        artist_name=data.get('artist_name'),
        genre=data.get('genre'),
        release_year=data.get('release_year'),
        album=data.get('album'),
        upload_date=None,  # Auto-set by DB
        duration=data.get('duration'),
        bitrate=data.get('bitrate'),
        file_path=data.get('file_path')
    )
    song_id = song_dao.add_song(song)
    if song_id:
        return jsonify({'song_id': song_id}), 201
    return jsonify({'error': 'Failed to add song'}), 500