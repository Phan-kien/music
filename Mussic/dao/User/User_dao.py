from typing import Optional
from mysql.connector import MySQLConnection, Error
from dao.User.User_interface import LoginInput, RegisterInput, User
from dao.User.User_object import User

class UserDAO(User):
    def __init__(self, db_connection: MySQLConnection):
        self.connection = db_connection

    def create_user(self, input_data: 'RegisterInput') -> Optional[User]:
        try:
            cursor = self.connection.cursor()
            # Tạm thời để nguyên mật khẩu (bạn nên thay thế bằng một hàm hash mới nếu cần)
            hashed_password = input_data.password
            query = """
                INSERT INTO User (User_Name, Email, Password, Registration_Date)
                VALUES (%s, %s, %s, NOW())
            """
            cursor.execute(query, (input_data.username, input_data.email, hashed_password))
            self.connection.commit()
            user_id = cursor.lastrowid
            return User(
                user_id=user_id,
                username=input_data.username,
                email=input_data.email,
                password=hashed_password,
                registration_date=None
            )
        except Error as e:
            print(f"Error creating user: {e}")
            return None
        finally:
            cursor.close()

    def get_user_by_username(self, username: str) -> Optional[User]:
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT User_ID, User_Name, Email, Password, Registration_Date
                FROM User
                WHERE User_Name = %s
            """
            cursor.execute(query, (username,))
            row = cursor.fetchone()
            if row:
                return User(
                    user_id=row[0],
                    username=row[1],
                    email=row[2],
                    password=row[3],
                    registration_date=row[4]
                )
            return None
        except Error as e:
            print(f"Error retrieving user by username: {e}")
            return None
        finally:
            cursor.close()

    def verify_user_credentials(self, input_data: 'LoginInput') -> Optional[User]:
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT User_ID, User_Name, Email, Password, Registration_Date
                FROM User
                WHERE User_Name = %s
            """
            cursor.execute(query, (input_data.username,))
            row = cursor.fetchone()
            if row and input_data.password == row[3]:  # So sánh trực tiếp (không hash nữa)
                return User(
                    user_id=row[0],
                    username=row[1],
                    email=row[2],
                    password=row[3],
                    registration_date=row[4]
                )
            return None
        except Error as e:
            print(f"Error verifying user credentials: {e}")
            return None
        finally:
            cursor.close()

    def store_token(self, user_id: int, token: str) -> bool:
        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE User
                SET Token = %s
                WHERE User_ID = %s
            """
            cursor.execute(query, (token, user_id))
            self.connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error storing token: {e}")
            return False
        finally:
            cursor.close()

    def clear_token(self, user_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE User
                SET Token = NULL
                WHERE User_ID = %s
            """
            cursor.execute(query, (user_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error clearing token: {e}")
            return False
        finally:
            cursor.close()
