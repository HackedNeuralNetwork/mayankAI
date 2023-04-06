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

