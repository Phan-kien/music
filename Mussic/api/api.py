from flask import Flask
from api.login_api import login_api
from api.register_api import register_api
from api.like_api import like_api
from api.playlist_api import playlist_api
from api.song_api import song_api

app = Flask(__name__)
# Đăng ký các API route
app.register_blueprint(login_api)
app.register_blueprint(register_api)
app.register_blueprint(like_api)
app.register_blueprint(playlist_api)
app.register_blueprint(song_api)
if __name__ == '__main__':
    app.run(debug=True)
