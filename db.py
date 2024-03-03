import sqlite3

class DBHelper:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            user_id TEXT)''')
        self.conn.commit()

    def add_user(self, user_id):
        self.cur.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        self.conn.commit()

    def get_user_by_user_id(self, user_id):
        self.cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        return self.cur.fetchone()

    def get_all_users(self):
        self.cur.execute("SELECT * FROM users")
        return self.cur.fetchall()

    def close(self):
        self.conn.close()
