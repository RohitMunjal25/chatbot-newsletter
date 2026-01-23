from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import find_answer
from db import get_connection
import os

app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")

    conn = get_connection()
    cur = conn.cursor()

    # save user message
    cur.execute(
        "INSERT INTO chat_logs (sender, message) VALUES (?, ?)",
        ("user", user_msg)
    )

    # email detection
    if "@" in user_msg and "." in user_msg:
        try:
            cur.execute(
                "INSERT INTO subscribers (email) VALUES (?)",
                (user_msg,)
            )
            reply = "You are subscribed to the newsletter!"
        except:
            reply = "This email is already subscribed."
    else:
        reply = find_answer(user_msg)

    if reply is None:
        reply = "Thanks for your message."

    # save bot reply
    cur.execute(
        "INSERT INTO chat_logs (sender, message) VALUES (?, ?)",
        ("bot", reply)
    )

    conn.commit()
    conn.close()

    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
