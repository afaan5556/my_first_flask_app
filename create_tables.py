import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS visitors (id INTEGER PRIMARY KEY, name text, first_name text, last_name text, email text, phone text)"
cursor.execute(create_table)

connection.commit()
connection.close()