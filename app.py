from flask import Flask, render_template,request,jsonify
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
def predict_next_outcome():
    last_10_results = get_last10game()
    high_count = last_10_results.count('High')
    low_count = last_10_results.count('Low')
    tie_count = last_10_results.count('Tie')

    if high_count > low_count and high_count > tie_count:
        return "Low Card"
    elif low_count > high_count and low_count > tie_count:
        return "High Card"
    else:
        return "Tie is High Card"


# Get Time and Game ID
@app.route("/get_data")
def get_data():
    time, g_id = get_time_gID()
    last10 = get_last10game()
    nextGame = predict_next_outcome()
    return jsonify({"time": time, "g_id": g_id, "last10": str(last10), "nextGame": nextGame})

if __name__ == "__main__":
    app.run(debug=True)