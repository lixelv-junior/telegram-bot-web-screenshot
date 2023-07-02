import sqlite3
from url import create_folder_if_not_exists

class SQL():

    def __init__(self, name):
        self.connect = sqlite3.connect(name)
        self.cursor = self.connect.cursor()
        self.do('''
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY UNIQUE,
    name TEXT,
    width INTEGER DEFAULT 1920,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);''')

    def is_new_user(self, user_id):
        return not bool(self.select('SELECT * FROM user WHERE id=?', (user_id,)))

    def add_user(self, user_id, user_name):
        self.do('INSERT INTO user (id, name) VALUES (?, ?)', (user_id, user_name))
        create_folder_if_not_exists(f'image/{user_id}')

    def select_width(self, user_id):
        return self.select('SELECT width FROM user WHERE id=?', (user_id,))[0][0]


    def do(self, sql, values=()):
        self.cursor.execute(sql, values)
        self.connect.commit()

    def select(self, sql, values):
        self.cursor.execute(sql, values)
        return self.cursor.fetchall()

sql = SQL('data.db')