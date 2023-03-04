from flask import Flask, render_template,request
import db
import requests
import os

app = Flask(__name__)
last_Games = []
last_Games1 = []
high_card = ("A","2","3","4","5","6")
low_card = ("8","9","10","J","Q","K")
guess_game = ""
result_game = ""
total_win = 0
total_loss = 0

# Home Page 
@app.route("/")
def index():
    return render_template("index.html") # Return Home HTML Page

@app.route("/resetsdb",methods=['POST','GET'])
def reset_db():
    if request.method == "POST":
        points = request.form["upoint"]
        db.delete_db()
        db.create_db()
        db.lucky7a("0","0",points,"0")
    return render_template("resetsdb.html")

# Game Page
@app.route("/lucky7a")
def lucky7a():   # retune Game HTMl Page
    user_balance = db.get_balance()[0][0]
    global last_Games, guess_game, last_Games1, result_game
    last_Games = []
    add_data() # Call Get Last 10 Game Result form Function
    guess_game = next_game(last_Games1)
    if last_Games != last_Games1:
        result_game = last_Games[0]
        last_Games1 = last_Games
        if guess_game == result_game:
            win = "You Win"
            user_balance += 200
            db.lucky7a(guess_game,result_game,user_balance,"Y")
        else:
            win = "You Loss"
            user_balance -= 100
            db.lucky7a(guess_game, result_game, user_balance, "N")
    else:
        last_Games1 = last_Games
        win = "Please Wait For the Result"

    # call Predict Next Game Function
    time = get_time()
    return render_template("lucky7a.html",next=guess_game,c_next=result_game,last=str(last_Games),c_last=str(last_Games1),bal=user_balance,t=time,w=win)

def add_data(): # Get Last 10 Game Results in Dictionary
    global last_Games, last_Games1
    try:
        data = requests.get(url='https://multiexch.com:3448/api/l_result/lucky7').json()
    except:
        return "Fuck we are Blocked, Now Call Yogendra!!"
    
    for i in data['data']:
        if i['result'] == '1':
            last_Games.append("Low")
        elif i['result'] == '2':
            last_Games.append("High")
        else:
            last_Games.append("Tie")
    if len(last_Games1) == 0:
        last_Games1 = last_Games.copy()

def next_game(game): # Predict Next Game Algo Function
    count_h = 0
    count_l = 0
    count_t = 0
    for i in last_Games:
        if i == "High":
            count_h += 1
        elif i == "Low":
            count_l +=1
        else:
            count_t +=1

    if count_h > count_t:
        return "Low"
    elif count_t > count_h:
        return "High"

def get_time():
    try:
        time = requests.get(url='https://multiexch.com:3448/api/d_rate/lucky7').json()
        c_time = time['data']['t1'][0]['autotime']  # Current Time in Game
        return c_time
    except:
        return "Fuck we are Blocked, Now Call Yogendra!!"

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

if __name__ == "__main__":
    app.run(debug=True)