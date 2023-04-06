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

def win_balance_db():
    balance = get_balance()[0][0]
    balance += 200
    conn = sqlite3.connect("ai.db")
    c = conn.cursor()
    c.execute("UPDATE lucky7a SET bal = ? WHERE id = (SELECT id FROM lucky7a ORDER BY id DESC LIMIT 1)", (balance,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    win_balance_db()
    print(get_balance())

