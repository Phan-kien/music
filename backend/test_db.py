# backend/test_db.py
from config.db import db
conn = db.connect()
if conn:
    print("Connection successful!")
    cursor = db.get_cursor()
    cursor.execute("SELECT 1")
    print("Query result:", cursor.fetchone())
    db.close()
else:
    print("Connection failed!")