<?php
$host = 'localhost';
$username = 'root';  // username mặc định của XAMPP là 'root'
$password = '';      // Mặc định không có mật khẩu
$dbname = 'music_db'; // Tên cơ sở dữ liệu mà bạn đã tạo

try {
    $conn = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    // set the PDO error mode to exception
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
?>
