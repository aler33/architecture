import sqlite3


con = sqlite3.connect('arch.sqlite3')
cur = con.cursor()
with open('create_db', 'r') as f:
    text = f.read()
    # print(text)
    cur.executescript(text)
cur.close()
con.close()
