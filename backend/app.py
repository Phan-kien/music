from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import logging
import pymysql
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Cấu hình CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Tạo thư mục uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
SONGS_FOLDER = os.path.join(UPLOAD_FOLDER, 'songs')
os.makedirs(SONGS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/music_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)

# User model
class User(db.Model):
    __tablename__ = 'User'
    
    id = db.Column('User_ID', db.Integer, primary_key=True)
    username = db.Column('User_Name', db.String(100), nullable=False, unique=True)
    email = db.Column('Email', db.String(100), nullable=False, unique=True)
    password = db.Column('Password', db.String(255), nullable=False)
    registration_date = db.Column('Registration_Date', db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    token = db.Column('Token', db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'registration_date': self.registration_date.isoformat() if self.registration_date else None
        }

# Song model
class Song(db.Model):
    __tablename__ = 'Song'
    
    id = db.Column('Song_ID', db.Integer, primary_key=True)
    user_id = db.Column('User_ID', db.Integer, db.ForeignKey('User.User_ID'), nullable=False)
    title = db.Column('Song_Name', db.String(255), nullable=False)
    artist = db.Column('ArtistName', db.String(255), nullable=False)
    genre = db.Column('Genre', db.String(100), nullable=False)
    release_year = db.Column('ReleaseYear', db.Integer)
    album = db.Column('Album', db.String(255))
    upload_date = db.Column('Upload_Date', db.DateTime, default=datetime.datetime.utcnow)
    duration = db.Column('Duration', db.Time)
    bitrate = db.Column('Bitrate', db.Integer)
    file_path = db.Column('File_Path', db.String(500), nullable=False)
    user = db.relationship('User', backref='songs')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'genre': self.genre,
            'release_year': self.release_year,
            'album': self.album,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'duration': str(self.duration) if self.duration else None,
            'bitrate': self.bitrate,
            'file_path': self.file_path,
            'user_id': self.user_id
        }

# Playlist model
class Playlist(db.Model):
    __tablename__ = 'Playlist'
    
    id = db.Column('Playlist_ID', db.Integer, primary_key=True)
    user_id = db.Column('User_ID', db.Integer, db.ForeignKey('User.User_ID'), nullable=False)
    name = db.Column('Playlist_Name', db.String(255), nullable=False)
    artist = db.Column('ArtistName', db.String(255))
    release_date = db.Column('ReleaseDate', db.Date)
    songs = db.relationship('Song', secondary='Belong_to', backref='playlists')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'artist': self.artist,
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'user_id': self.user_id,
            'songs': [song.to_dict() for song in self.songs]
        }

# LikedSongs model
class LikedSongs(db.Model):
    __tablename__ = 'LikedSongs'
    
    user_id = db.Column('User_ID', db.Integer, db.ForeignKey('User.User_ID'), primary_key=True)
    song_id = db.Column('Song_ID', db.Integer, db.ForeignKey('Song.Song_ID'), primary_key=True)
    liked_at = db.Column('Liked_At', db.DateTime, default=datetime.datetime.utcnow)

# Belong_to model
class BelongTo(db.Model):
    __tablename__ = 'Belong_to'
    
    song_id = db.Column('Song_ID', db.Integer, db.ForeignKey('Song.Song_ID'), primary_key=True)
    playlist_id = db.Column('Playlist_ID', db.Integer, db.ForeignKey('Playlist.Playlist_ID'), primary_key=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def get_user_from_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return User.query.get(payload['user_id'])
    except:
        return None

@app.route('/api/register', methods=['POST'])
def register():
    try:
        logger.debug('Received registration request')
        data = request.get_json()
        logger.debug(f'Registration data: {data}')

        # Validate required fields
        if not all(k in data for k in ['username', 'email', 'password']):
            logger.error('Missing required fields')
            return jsonify({'detail': 'Missing required fields'}), 400

        # Validate username
        if not isinstance(data['username'], str) or len(data['username']) < 3 or len(data['username']) > 100:
            logger.error('Invalid username')
            return jsonify({'detail': 'Username must be between 3 and 100 characters'}), 422

        # Validate email
        if not isinstance(data['email'], str) or '@' not in data['email']:
            logger.error('Invalid email')
            return jsonify({'detail': 'Invalid email format'}), 422

        # Validate password
        if not isinstance(data['password'], str) or len(data['password']) < 6:
            logger.error('Invalid password')
            return jsonify({'detail': 'Password must be at least 6 characters long'}), 422

        # Check if username already exists
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            logger.error(f'Username already exists: {data["username"]}')
            return jsonify({'detail': 'Username already exists'}), 422

        # Check if email already exists
        existing_email = User.query.filter_by(email=data['email']).first()
        if existing_email:
            logger.error(f'Email already exists: {data["email"]}')
            return jsonify({'detail': 'Email already exists'}), 422

        # Create new user
        hashed_password = generate_password_hash(data['password'])
        logger.debug(f'Generated hashed password: {hashed_password}')
        
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=hashed_password
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            logger.info(f'User registered successfully: {new_user.username}')
            logger.debug(f'User data: {new_user.to_dict()}')
            return jsonify(new_user.to_dict()), 201
        except Exception as db_error:
            logger.error(f'Database error during registration: {str(db_error)}')
            db.session.rollback()
            return jsonify({'detail': 'Database error during registration'}), 500

    except Exception as e:
        logger.error(f'Registration error: {str(e)}')
        db.session.rollback()
        return jsonify({'detail': 'Internal server error'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        logger.debug('Received login request')
        data = request.get_json()
        logger.debug(f'Login data: {data}')

        if not all(k in data for k in ['username', 'password']):
            logger.error('Missing required fields')
            return jsonify({'detail': 'Missing required fields'}), 400

        user = User.query.filter_by(username=data['username']).first()
        logger.debug(f'Found user: {user.to_dict() if user else None}')

        if not user:
            logger.error(f'User not found: {data["username"]}')
            return jsonify({'detail': 'Invalid username or password'}), 401

        if not check_password_hash(user.password, data['password']):
            logger.error(f'Invalid password for user: {data["username"]}')
            return jsonify({'detail': 'Invalid username or password'}), 401

        token = generate_token(user.id)
        logger.info(f'User logged in successfully: {user.username}')
        logger.debug(f'Generated token: {token}')

        return jsonify({
            'token': token,
            'user': user.to_dict()
        }), 200

    except Exception as e:
        logger.error(f'Login error: {str(e)}')
        return jsonify({'detail': 'Internal server error'}), 500

@app.route('/api/songs/upload', methods=['POST'])
def upload_song():
    try:
        user = get_user_from_token()
        if not user:
            logger.error('Unauthorized: No valid token found')
            return jsonify({'detail': 'Unauthorized'}), 401

        logger.debug('Received song upload request')
        
        if 'file' not in request.files:
            logger.error('No file part in request')
            return jsonify({'detail': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            logger.error('No selected file')
            return jsonify({'detail': 'No selected file'}), 400

        if not allowed_file(file.filename):
            logger.error(f'Invalid file type: {file.filename}')
            return jsonify({'detail': 'File type not allowed'}), 400

        try:
            # Generate unique filename
            filename = secure_filename(file.filename)
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{timestamp}_{filename}"
            file_path = os.path.join(SONGS_FOLDER, unique_filename)
            
            # Save file
            file.save(file_path)
            logger.info(f'File saved successfully: {file_path}')

            # Get song info from form
            title = request.form.get('title')
            artist = request.form.get('artist')
            genre = request.form.get('genre')
            release_year = request.form.get('release_year')
            album = request.form.get('album')

            # Validate and set default values
            if not title:
                title = os.path.splitext(filename)[0]
            if not artist:
                artist = 'Unknown Artist'
            if not genre:
                genre = 'Unknown'
            if not album:
                album = 'Unknown'

            # Convert release_year to integer if it exists
            if release_year and release_year.isdigit():
                release_year = int(release_year)
            else:
                release_year = None

            logger.debug(f'Song metadata: title={title}, artist={artist}, genre={genre}, year={release_year}, album={album}')

            # Create song record
            song = Song(
                title=title,
                artist=artist,
                genre=genre,
                release_year=release_year,
                album=album,
                file_path=f'/api/songs/file/{unique_filename}',
                user_id=user.id,
                upload_date=datetime.datetime.utcnow()
            )

            db.session.add(song)
            db.session.commit()
            logger.info(f'Song created successfully: {song.title} for user {user.username}')
            return jsonify(song.to_dict()), 201

        except Exception as db_error:
            logger.error(f'Error saving file or creating song: {str(db_error)}')
            if os.path.exists(file_path):
                os.remove(file_path)
            db.session.rollback()
            return jsonify({'detail': 'Error saving file or creating song'}), 500

    except Exception as e:
        logger.error(f'Error uploading song: {str(e)}')
        return jsonify({'detail': 'Internal server error'}), 500

@app.route('/api/songs/file/<filename>')
def serve_song(filename):
    try:
        # Allow public access to song files
        return send_from_directory(SONGS_FOLDER, filename)
    except Exception as e:
        logger.error(f'Error serving song: {str(e)}')
        return jsonify({'detail': 'File not found'}), 404

@app.route('/api/songs', methods=['GET'])
def get_songs():
    try:
        user = get_user_from_token()
        if not user:
            return jsonify({'detail': 'Unauthorized'}), 401

        songs = Song.query.filter_by(user_id=user.id).order_by(Song.upload_date.desc()).all()
        return jsonify([song.to_dict() for song in songs])
    except Exception as e:
        logger.error(f'Error getting songs: {str(e)}')
        return jsonify({'detail': 'Internal server error'}), 500

@app.route('/api/playlists', methods=['GET'])
def get_playlists():
    try:
        user = get_user_from_token()
        if not user:
            return jsonify({'detail': 'Unauthorized'}), 401

        playlists = Playlist.query.filter_by(user_id=user.id).all()
        return jsonify([playlist.to_dict() for playlist in playlists]), 200

    except Exception as e:
        logger.error(f'Error fetching playlists: {str(e)}')
        return jsonify({'detail': 'Internal server error'}), 500

@app.route('/api/playlists', methods=['POST'])
def create_playlist():
    try:
        user = get_user_from_token()
        if not user:
            logger.error('Unauthorized: No valid token found')
            return jsonify({'detail': 'Unauthorized'}), 401

        data = request.get_json()
        logger.debug(f'Received playlist creation request: {data}')
        
        if not data or 'name' not in data:
            logger.error('Missing playlist name in request')
            return jsonify({'detail': 'Playlist name is required'}), 400

        playlist = Playlist(
            name=data['name'],
            artist='Various Artists',  # Mặc định
            user_id=user.id
        )

        try:
            db.session.add(playlist)
            db.session.commit()
            logger.info(f'Playlist created successfully: {playlist.name} for user {user.username}')
            return jsonify(playlist.to_dict()), 201
        except Exception as db_error:
            logger.error(f'Database error creating playlist: {str(db_error)}')
            db.session.rollback()
            return jsonify({'detail': 'Database error creating playlist'}), 500

    except Exception as e:
        logger.error(f'Error creating playlist: {str(e)}')
        return jsonify({'detail': 'Internal server error'}), 500

@app.route('/api/playlists/<int:playlist_id>/songs', methods=['POST'])
def add_song_to_playlist(playlist_id):
    try:
        user = get_user_from_token()
        if not user:
            return jsonify({'detail': 'Unauthorized'}), 401

        playlist = Playlist.query.get_or_404(playlist_id)
        if playlist.user_id != user.id:
            return jsonify({'detail': 'Unauthorized'}), 401

        data = request.get_json()
        if not data or 'song_id' not in data:
            return jsonify({'detail': 'Song ID is required'}), 400

        song = Song.query.get_or_404(data['song_id'])
        if song.user_id != user.id:
            return jsonify({'detail': 'Unauthorized'}), 401

        playlist.songs.append(song)
        db.session.commit()

        return jsonify(playlist.to_dict()), 200

    except Exception as e:
        logger.error(f'Error adding song to playlist: {str(e)}')
        return jsonify({'detail': 'Internal server error'}), 500

@app.route('/api/songs/<int:song_id>', methods=['GET'])
def get_song_by_id(song_id):
    try:
        song = Song.query.get_or_404(song_id)
        # Return song info without requiring authentication
        return jsonify(song.to_dict())
    except Exception as e:
        logger.error(f'Error getting song: {str(e)}')
        return jsonify({'detail': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 