import sqlite3
from models.feed import Story, Source


def initialize():
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS
                    sources(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    url TEXT, 
                    name TEXT
                    );""")
        res = cur.execute("SELECT * FROM sources")
        for entry in res.fetchall():
            s = Source(entry[0], entry[1], entry[2])
            sourceList.append(s)
        cur.close()

def addSource(s: Source):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO sources(url, name) VALUES (?, ?)", (s.url, s.name))
        con.commit()
        s.id = cur.lastrowid
        sourceList.append(s)

def delSource(s: Source):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM sources WHERE id=?;", (s.id,))
        con.commit()
        sourceList.remove(s)

sourceList = []
initialize()
