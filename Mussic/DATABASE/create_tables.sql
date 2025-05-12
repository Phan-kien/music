
CREATE TABLE User (
    User_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE, 
    Password VARCHAR(255) NOT NULL,
    Registration_Date DATETIME NOT NULL
);

CREATE TABLE Song (
    Song_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID INT NOT NULL,                        -- Người dùng đã thêm bài hát
    Song_Name VARCHAR(255) NULL,
    ArtistName VARCHAR(255) NULL,
    Genre VARCHAR(100) NULL,
    ReleaseYear YEAR NULL,
    Album VARCHAR(255),
	Upload_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    Duration TIME,                               -- Thời lượng bài hát
    Bitrate INT,                                 -- Tốc độ bit (kbps)
    File_Path VARCHAR(500) NOT NULL,             -- Đường dẫn tới file âm thanh
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) -- Khóa ngoại tham chiếu đến bảng User
);


CREATE TABLE Playlist (
    Playlist_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID INT NOT NULL, -- người dùng tạo playlist
    Playlist_Name VARCHAR(255) NOT NULL,
    ArtistName VARCHAR(255), -- có thể NULL nếu playlist tổng hợp nhiều nghệ sĩ
    ReleaseDate DATE NULL,
    FOREIGN KEY (User_ID) REFERENCES User(User_ID)
);

CREATE TABLE LikedSongs (
    User_ID INT NOT NULL,
    Song_ID INT NOT NULL,
    Liked_At DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (User_ID, Song_ID),
    FOREIGN KEY (User_ID) REFERENCES User(User_ID),
    FOREIGN KEY (Song_ID) REFERENCES Song(Song_ID)
);


CREATE TABLE Belong_to (
    Song_ID INT NOT NULL,
    Playlist_ID INT NOT NULL,
    PRIMARY KEY (Song_ID, Playlist_ID),
    FOREIGN KEY (Song_ID) REFERENCES Song(Song_ID),
    FOREIGN KEY (Playlist_ID) REFERENCES Playlist(Playlist_ID)
);
