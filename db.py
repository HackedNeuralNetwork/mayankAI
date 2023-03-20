import sqlite3
import os

"""
Creating Database and Tables Name
"""
def create_db():
    conn = sqlite3.connect("ai.db")
    c = conn.cursor()
    c.execute(""" CREATE TABLE lucky7a (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guess_game TEXT,
        game_result TEXT,
        bal INTEGER,
        win TEXT)
        """)
    conn.commit()
    conn.close()
    print("Create Data Successfully")

"""
Insert Data Into Tables
"""
def lucky7a(guess_game,game_result,bal,win):
    conn = sqlite3.connect("ai.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO lucky7a (guess_game,game_result,bal,win) VALUES ('{}','{}',{},'{}')".format(guess_game,game_result,bal,win))
    except:
        pass
    conn.commit()
    conn.close()


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

"""
Delete Database
"""
def delete_db():
    conn = sqlite3.connect("ai.db")
    c = conn.cursor()
    try:
        c.execute(""" DROP TABLE lucky7a """)
        c.execute(""" CREATE TABLE lucky7a (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guess_game TEXT,
                game_result TEXT,
                bal INTEGER,
                win TEXT)
                """)
    except:
        c.execute(""" CREATE TABLE lucky7a (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guess_game TEXT,
                game_result TEXT,
                bal INTEGER,
                win TEXT)
                """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    pass
    #create_db()
    # lucky7a("0","0",500,"0")
    # r = get_balance()[0][0]
    # update_data("Low")
    # r = get_win()
    # for i in r:
    #     print(i[0])
    #delete_db()

