import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv 

# Load biến môi trường từ file .env (nếu có)
load_dotenv()

class Database:
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'music_db'),
            'raise_on_warnings': True
        }
        self.connection = None

    def connect(self):
        """
        Kết nối tới MySQL nếu chưa có kết nối.
        
        Returns:
            MySQLConnection: Kết nối MySQL hoặc None nếu thất bại.
        """
        if self.connection and self.connection.is_connected():
            return self.connection
        
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("Connected to MySQL database")
                return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None
            return None

    def close(self):
        """
        Đóng kết nối MySQL nếu đang mở.
        """
        if self.connection and self.connection.is_connected():
            try:
                self.connection.close()
                print("MySQL connection closed")
            except Error as e:
                print(f"Error closing MySQL connection: {e}")
            finally:
                self.connection = None

    def get_cursor(self):
        """
        Lấy cursor từ kết nối hiện tại.
        
        Returns:
            Cursor: Cursor trả về kết quả dạng dictionary, hoặc None nếu không có kết nối.
        """
        if self.connection and self.connection.is_connected():
            return self.connection.cursor(dictionary=True)
        return None

    def is_connected(self):
        """
        Kiểm tra xem kết nối có đang hoạt động hay không.
        
        Returns:
            bool: True nếu kết nối đang mở, False nếu không.
        """
        return self.connection is not None and self.connection.is_connected()

# Khởi tạo một instance chung
db = Database()