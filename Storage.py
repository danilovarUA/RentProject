import sqlite3

DATABASE_NAME = 'rentDatabase.db'


class Database:
    def __init__(self):
        connection = sqlite3.connect(DATABASE_NAME)
        self.cursor = connection.cursor()
