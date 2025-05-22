import sqlite3

# Create a new SQLite database file
connection = sqlite3.connect('src/core/services/database.db')
connection.close()