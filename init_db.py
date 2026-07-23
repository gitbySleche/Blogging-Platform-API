import sqlite3

connection = sqlite3.connect('blog.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, category TEXT, tags TEXT, created_at TEXT, updated_at TEXT)')
connection.commit()
connection.close()

