from flask import Flask, request, jsonify, send_from_directory
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("cafe.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            message TEXT
        )
    """)

    conn.close()


@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/<path:filename>")
def files(filename):
    return send_from_directory(".", filename)

@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json()

    name = data.get("name")
    message = data.get("message")

    conn = sqlite3.connect("cafe.db")

    conn.execute(
        "INSERT INTO contacts (name, message) VALUES (?, ?)",
        (name, message)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": f"{name}さん、お問い合わせを保存しました！"
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)