<?php
// Lấy đường dẫn từ URL
$request = $_SERVER['REQUEST_URI'];  

// Định tuyến yêu cầu đến các file API tương ứng
if (strpos($request, '/user/login') !== false) {
    include 'user/login.php';
} elseif (strpos($request, '/user/register') !== false) {
    include 'user/register.php';
} elseif (strpos($request, '/song/list') !== false) {
    include 'song/list.php';
} elseif (strpos($request, '/playlist/create') !== false) {
    include 'playlist/create.php';
} elseif (strpos($request, '/listen/record') !== false) {
    include 'listen/listen_song.php';
} else {
    echo "404 Not Found";
}
?>
