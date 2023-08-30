import sqlite3
import pandas as pd

conn = sqlite3.connect('mydatabase.db')

cur = conn.cursor()

# Query the SQLite master table for the names of all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Extract the table names from the cursor object
table_names = [row[0] for row in cur.fetchall()]

# Close the database connection


# Print the table names
print(table_names)

cursor = conn.execute(f"SELECT * FROM {table_names[6]};")
rows = cursor.fetchall()



for row in rows:
    print(row)



df = pd.read_sql(f'SELECT * FROM {table_names[6]}', conn)

# Print the DataFrame
print(df)

conn.close()