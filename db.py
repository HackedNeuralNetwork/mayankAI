import sqlite3

"""
Get Data
"""
def get_results():
    conn = sqlite3.connect("ai.db")
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM lucky7a")
    except:
        pass
    rows = c.fetchall()
    conn.commit()
    conn.close()
    return rows

def get_balance():
    conn = sqlite3.connect("ai.db")
    c = conn.cursor()
    try:
        c.execute("SELECT bal FROM lucky7a ORDER BY id DESC LIMIT 1")
    except:
        pass
    rows = c.fetchall()
    conn.commit()
    conn.close()
    return rows



def get_win():
    conn = sqlite3.connect("ai.db")
    c = conn.cursor()
    try:
        c.execute("SELECT win FROM lucky7a")
    except:
        pass

    rows = c.fetchall()
    conn.commit()
    conn.close()
    return rows

def create_db():
    conn = sqlite3.connect("ai.db")
    c = conn.cursor()
    c.execute(""" CREATE TABLE results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        last10 TEXT)
        """)
    conn.commit()
    conn.close()

def insert_last10_results(result):
    conn = sqlite3.connect("ai.db")
    c = conn.cursor()
    c.execute("INSERT INTO results (last10) VALUES (?)", (result,))
    conn.commit()
    conn.close()



if __name__ == "__main__":
    create_db()
    # last10 = 'LHTHHHLLHH'
    # insert_last10_results(last10)

