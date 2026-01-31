from flask import Flask, request, jsonify, render_template, abort
from flask_cors import CORS
from chatbot import find_answer
from db import get_connection
import os
import json

app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO chat_logs (sender, message) VALUES (?, ?)",
        ("user", user_msg)
    )

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
    
    reply_to_save=reply
    if isinstance(reply,dict):
        reply_to_save=json.dumps(reply)

    cur.execute(
        "INSERT INTO chat_logs (sender, message) VALUES (?, ?)",
        ("bot", reply_to_save)
    )

    conn.commit()
    conn.close()

    if isinstance(reply,dict):
        return jsonify({"reply": reply.get("image") or reply.get("text")})

    return jsonify({"reply":reply})

@app.route("/admin", methods=["GET"])
def admin():
    if request.args.get("key") != "admin123":
        abort(403)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM subscribers ORDER BY created_at DESC")
    subscribers = cur.fetchall()

    cur.execute("SELECT * FROM chat_logs ORDER BY created_at DESC LIMIT 100")
    chat_logs = cur.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        subscribers=subscribers,
        chat_logs=chat_logs
    )
@app.route("/health", methods=["GET", "POST"])
def health():
    return jsonify({"status": "alive"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
