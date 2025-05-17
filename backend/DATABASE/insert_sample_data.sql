-- Dữ liệu mẫu cho bảng User
INSERT INTO User (User_Name, Email, Password, Token)
VALUES
('alice123', 'alice@example.com', 'password1', NULL),
('bob456', 'bob@example.com', 'password2', NULL),
('charlie789', 'charlie@example.com', 'password3', NULL);

-- Dữ liệu mẫu cho bảng Song
INSERT INTO Song (User_ID, Song_Name, ArtistName, Genre, ReleaseYear, Album, Duration, Bitrate, File_Path)
VALUES
(1, 'Let It Be', 'The Beatles', 'Rock', 1970, 'Let It Be', '00:03:50', 320, 'audio/let_it_be.mp3'),
(2, 'Blinding Lights', 'The Weeknd', 'Pop', 2020, 'After Hours', '00:03:20', 320, 'audio/blinding_lights.mp3'),
(3, 'Shape of You', 'Ed Sheeran', 'Pop', 2017, 'Divide', '00:03:54', 320, 'audio/shape_of_you.mp3');

-- Dữ liệu mẫu cho bảng Playlist
INSERT INTO Playlist (User_ID, Playlist_Name, ArtistName, ReleaseDate)
VALUES
(1, 'Relaxing Rock', 'Various Artists', '2023-01-01'),
(2, 'Top Pop Hits', 'Various Artists', '2024-01-15');

-- Dữ liệu mẫu cho bảng LikedSongs
INSERT INTO LikedSongs (User_ID, Song_ID)
VALUES
(1, 2),
(1, 3),
(2, 1),
(3, 1),
(3, 2);

-- Dữ liệu mẫu cho bảng Belong_to
INSERT INTO Belong_to (Song_ID, Playlist_ID)
VALUES
(1, 1),
(2, 2),
(3, 2);
