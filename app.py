from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import find_answer
from db import subscribers_col, chatlogs_col
import datetime
import os

app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")

    
    chatlogs_col.insert_one({
        "sender": "user",
        "message": user_msg,
        "time": datetime.datetime.utcnow()
    })

    if "@" in user_msg and "." in user_msg:
        subscribers_col.insert_one({
            "email": user_msg,
            "subscribed_at": datetime.datetime.utcnow()
        })
        reply = "You are subscribed to the newsletter!"
    else:
        reply = find_answer(user_msg)

    if reply is None:
        reply = "Thanks for your message."

    chatlogs_col.insert_one({
        "sender": "bot",
        "message": reply,
        "time": datetime.datetime.utcnow()
    })

    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
