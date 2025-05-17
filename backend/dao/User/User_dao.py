from typing import Optional
from fastapi import HTTPException
from mysql.connector import MySQLConnection, Error
from dao.User.User_interface import LoginInput, RegisterInput, User
from dao.User.User_object import User as UserObject

class UserDAO:
    def __init__(self, db_connection: MySQLConnection):
        self.connection = db_connection

    def create_user(self, input_data: RegisterInput) -> Optional[User]:
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Kiểm tra username đã tồn tại
            cursor.execute("SELECT User_ID FROM User WHERE User_Name = %s", (input_data.username,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Username already exists")
            
            # Kiểm tra email đã tồn tại
            cursor.execute("SELECT User_ID FROM User WHERE Email = %s", (input_data.email,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Email already exists")
            
            query = """
                INSERT INTO User (User_Name, Email, Password, Registration_Date)
                VALUES (%s, %s, %s, NOW())
            """
            cursor.execute(query, (input_data.username, input_data.email, input_data.password))
            self.connection.commit()
            user_id = cursor.lastrowid
            
            cursor.execute("SELECT User_ID, User_Name, Email, Registration_Date FROM User WHERE User_ID = %s", (user_id,))
            row = cursor.fetchone()
            if row:
                return User(
                    user_id=row['User_ID'],
                    username=row['User_Name'],
                    email=row['Email'],
                    registration_date=row['Registration_Date']
                )
            return None
        except Error as e:
            print(f"Error creating user: {e}")
            raise HTTPException(status_code=500, detail="Database error occurred")
        finally:
            cursor.close()

    def get_user_by_username(self, username: str) -> Optional[UserObject]:
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT User_ID, User_Name, Email, Password, Registration_Date
                FROM User
                WHERE User_Name = %s
            """
            cursor.execute(query, (username,))
            row = cursor.fetchone()
            if row:
                return UserObject(
                    user_id=row['User_ID'],
                    username=row['User_Name'],
                    email=row['Email'],
                    password=row['Password'],
                    registration_date=row['Registration_Date']
                )
            return None
        except Error as e:
            print(f"Error retrieving user by username: {e}")
            raise HTTPException(status_code=500, detail="Database error occurred")
        finally:
            cursor.close()

    def verify_user_credentials(self, input_data: LoginInput) -> Optional[UserObject]:
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT User_ID, User_Name, Email, Password, Registration_Date
                FROM User
                WHERE User_Name = %s
            """
            cursor.execute(query, (input_data.username,))
            row = cursor.fetchone()
            if row:
                return UserObject(
                    user_id=row['User_ID'],
                    username=row['User_Name'],
                    email=row['Email'],
                    password=row['Password'],
                    registration_date=row['Registration_Date']
                )
            return None
        except Error as e:
            print(f"Error verifying user credentials: {e}")
            raise HTTPException(status_code=500, detail="Database error occurred")
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
