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
    reply=find_answer(user_msg)

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
        return jsonify({
            "reply":{
                "text":reply.get("text"),
                "image":reply.get("image"),
                "video":reply.get("video")
            }
        })
    return jsonify({"reply":reply})
@app.route("/admin", methods=["GET"])
def admin():
    if request.args.get("key") != "admin123":
        abort(403)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM subscribers ORDER BY id DESC")
    subscribers = cur.fetchall()

    cur.execute("SELECT * FROM chat_logs ORDER BY id DESC LIMIT 100")
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
@app.route("/api/subscribe", methods=["POST"])
def subscribe():
    email = request.json.get("email")

    if not email or "@" not in email:
        return jsonify({"status": "error", "message": "Invalid email"}), 400

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO subscribers (email) VALUES (?)",
            (email,)
        )
        conn.commit()
        return jsonify({"status": "success"})
    except:
        return jsonify({"status": "exists"})
    finally:
        conn.close()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
