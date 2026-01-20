from flask import Flask, request, jsonify
from chatbot import find_answer
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")

    
    with open("chat_logs.txt", "a") as log:
        log.write(f"{datetime.datetime.now()} | USER: {user_msg}\n")


    if "@" in user_msg and "." in user_msg:
        with open("subscribers.txt", "a") as f:
            f.write(user_msg + "\n")
        reply = "You are subscribed to the newsletter!"
    else:
        reply = find_answer(user_msg)

    if reply is None:
        reply = "Thanks for your message! We'll include this in future updates."

    
    with open("chat_logs.txt", "a") as log:
        log.write(f"{datetime.datetime.now()} | BOT: {reply}\n")

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
