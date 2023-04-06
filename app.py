from flask import Flask, render_template,request,jsonify
import sqlite3
import db
import requests


app = Flask(__name__)
last_Games1 = []
high_card = ("A","2","3","4","5","6")
low_card = ("8","9","10","J","Q","K")
guess_game = ""
result_game = ""
total_win = 0
total_loss = 0



def get_time_gID():
    data = requests.get("https://multiexch.com:3448/api/d_rate/lucky7").json()
    data = data['data']['t1'][0]
    time = data['autotime']
    g_id = data['mid']
    return time, g_id

def get_last10game():
    last_Games = []
    data = requests.get(url='https://multiexch.com:3448/api/l_result/lucky7').json()

    for i in data['data']:
        if i['result'] == '1':
            last_Games.append("Low")
        elif i['result'] == '2':
            last_Games.append("High")
        else:
            last_Games.append("Tie")
    return last_Games



# Home Page
@app.route("/")
def index():
    return render_template("index.html") # Return Home HTML Page

# Reset DB
@app.route("/resetsdb",methods=['POST','GET'])
def reset_db():
    return render_template("resetsdb.html")

# Lucky 7A Game Page
@app.route("/lucky7a")
def lucky7a():   # retune Game HTMl Page
    return render_template("lucky7a.html")

@app.route("/next",methods=['POST'])
def calculate_weighted_probabilities():
    game_results = get_last10game()
    recent_games = game_results[:5]
    less_recent_games = game_results[5:]

    recent_weight = 0.6
    less_recent_weight = 0.4

    outcomes = ["High", "Low", "Tie"]
    counts = {outcome: [0, 0] for outcome in outcomes}

    for outcome in outcomes:
        counts[outcome][0] = recent_games.count(outcome)
        counts[outcome][1] = less_recent_games.count(outcome)

    weighted_probabilities = {
        outcome: (counts[outcome][0] * recent_weight + counts[outcome][1] * less_recent_weight) / 10
        for outcome in outcomes
    }
    return str(weighted_probabilities)


# Get Time and Game ID
@app.route("/get_data")
def get_data():
    time, g_id = get_time_gID()
    last10 = get_last10game()
    user_balance = db.get_balance()[0][0]
    nextGame = calculate_weighted_probabilities()
    if "Tie" in last10:
        return jsonify({"time": time, "g_id": g_id, "last10": str(last10), "balance": user_balance, "nextGame": "Wait Tie Card in last 10 Game"})
    else:
        return jsonify({"time": time, "g_id": g_id, "last10": str(last10), "balance": user_balance, "nextGame": nextGame})



# Result Page
@app.route("/result")
def result():
    data = db.get_results()
    c_ac,w_win = get_Accuracy()
    return render_template("results.html",data=data,ac=c_ac,w_in=w_win)

def get_Accuracy():
    global total_win,total_loss
    total_win = 0
    total_loss = 0
    getwin = db.get_win()
    for i in getwin:
        if i[0] == "Y":
            total_win += 1
        elif i[0] =="N":
            total_loss += 1

    if total_win > total_loss:
        ac = total_win/len(getwin)*100
        return ac,"win"
    elif total_win == total_loss:
        return 50,"win"
    else:
        ac = total_loss/len(getwin)*100
        return ac,"Loss"

@app.route('/bet',methods=['POST'])
def update_balance_db():
    balance = db.get_balance()[0][0]
    balance -= 100
    conn = sqlite3.connect("ai.db")
    c = conn.cursor()
    c.execute("UPDATE lucky7a SET bal = ? ORDER BY id DESC LIMIT 1", (balance))
    conn.commit()
    conn.close()

@app.route('/win',methods=['POST'])
def win_balance_db():
    balance = db.get_balance()[0][0]
    balance += 200
    conn = sqlite3.connect("ai.db")
    c = conn.cursor()
    c.execute("UPDATE lucky7a SET bal = ? ORDER BY id DESC LIMIT 1", (balance))
    conn.commit()
    conn.close()

@app.route('/create_db', methods=['POST'])
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
    return render_template("index.html")

@app.route('/insert_data', methods=['POST'])
def insert_data():
    guess_game = request.form['guess_game']
    game_result = request.form['game_result']
    bal = int(request.form['bal'])
    win = request.form['win']
    conn = sqlite3.connect("ai.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO lucky7a (guess_game,game_result,bal,win) VALUES ('{}','{}',{},'{}')".format(guess_game, game_result, bal, win))
    except:
        pass
    conn.commit()
    conn.close()
    return render_template("index.html")

@app.route('/delete_db', methods=['POST'])
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
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)