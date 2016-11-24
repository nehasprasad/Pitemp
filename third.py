import sqlite3
conn = sqlite3.connect('tweepy.db')

c = conn.cursor()

c.execute('''CREATE TABLE analysis
                (id INTEGER PRIMARY KEY AUTOINCREMENT, date text, temp real, condition1 text,  humidity real, condition2 text)''')

conn.commit()
conn.close()
