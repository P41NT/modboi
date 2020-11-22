import sqlite3

conn = sqlite3.connect("info.db")
c = conn.cursor()
# print(c.fetchall())
c.execute(f"SELECT *  FROM info WHERE action='KICK'")
print(c.fetchall())