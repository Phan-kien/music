-- Dữ liệu mẫu cho bảng User
INSERT INTO User (User_Name, Email, Password, Registration_Date)
VALUES 
('nghia123', 'nghia@example.com', '123456', NOW()),
('linh_yt', 'linh@example.com', 'abcxyz', NOW()),
('hoang_an', 'hoangan@example.com', 'password123', NOW());

-- Dữ liệu mẫu cho bảng Song
INSERT INTO Song (Song_Name, ArtistName, Genre, ReleaseYear, Duration, Bitrate, File_Path)
VALUES 
('Hoa Bằng Lăng', 'Trịnh Công Sơn', 'Trữ tình', 1990, '00:02:13', 320, '/audio/hoa-bang-lang.mp3'),
('Buông Đôi Tay Nhau Ra', 'Sơn Tùng M-TP', 'Pop', 2015, '00:02:55', 320, '/audio/buong-doi-tay-nhau-ra.mp3');

-- Dữ liệu mẫu cho bảng Playlist
INSERT INTO Playlist (User_ID, Playlist_Name, ArtistName, ReleaseDate)
VALUES 
(1, 'Tình Ca Trịnh', 'Trịnh Công Sơn', '1990-05-01'),
(1, 'Nhạc trẻ 2010s', NULL, '2015-08-10');

-- Dữ liệu mẫu cho bảng Belong_to
INSERT INTO Belong_to (Song_ID, Playlist_ID)
VALUES 
(1, 1),
(2, 2);

-- Dữ liệu mẫu cho bảng LikedSongs
INSERT INTO LikedSongs (User_ID, Song_ID)
VALUES 
(1, 1),
(1, 2);

-- Dữ liệu mẫu cho bảng Listen
INSERT INTO Listen (User_ID, Song_ID)
VALUES 
(1, 1),
(1, 2),
(2, 1);

-- Dữ liệu mẫu cho bảng UserSharedSongs (Chia sẻ bài hát với người dùng khác)
INSERT INTO UserSharedSongs (Song_ID, Sender_User_ID, Receiver_User_ID, Shared_At)
VALUES 
(1, 1, 2, NOW()),  -- Người dùng 1 chia sẻ bài hát 1 với người dùng 2
(2, 1, 3, NOW());  -- Người dùng 1 chia sẻ bài hát 2 với người dùng 3

-- Dữ liệu mẫu cho bảng GroupSharedSongs (Chia sẻ bài hát trong nhóm)
-- Giả sử nhóm có ID là 1
INSERT INTO GroupSharedSongs (Song_ID, Sender_User_ID, Group_ID, Shared_At)
VALUES 
(1, 1, 1, NOW()),  -- Người dùng 1 chia sẻ bài hát 1 trong nhóm 1
(2, 2, 1, NOW());  -- Người dùng 2 chia sẻ bài hát 2 trong nhóm 1

-- Dữ liệu mẫu cho bảng PublicSharedSongs (Chia sẻ bài hát công khai)
INSERT INTO PublicSharedSongs (Song_ID, Sender_User_ID, Shared_At)
VALUES 
(1, 1, NOW()),  -- Người dùng 1 chia sẻ bài hát 1 công khai
(2, 2, NOW());  -- Người dùng 2 chia sẻ bài hát 2 công khai
