import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

connection.commit()
connection.close()

# user = (1, 'afaan.naqvi', 'asdf')

# insert_query = "INSERT INTO users VALUES (?, ?, ?)"
# cursor.execute(insert_query, user)


# users = [
# 	(2, 'nida.jafri', 'qwer'),
# 	(3, 'jap.shap', 'zxcv'),
# 	(4, 'hop.scotch', 'qazx')
# ]

# cursor.executemany(insert_query, users)

# select_query = "SELECT * FROM users"

# for row in cursor.execute(select_query):
# 	print(row)
