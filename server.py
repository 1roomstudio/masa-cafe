from contextlib import closing
from pathlib import Path
import os
import sqlite3

from flask import Flask, abort, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
# 保存先は環境変数で変更可能。ローカルでは既存のcafe.dbを使います。
DB_PATH = Path(os.environ.get("DATABASE_PATH", str(BASE_DIR / "cafe.db")))
app = Flask(__name__, static_folder=None)


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                message TEXT
            )
        """)


# Gunicornから読み込まれた場合にも、テーブルを準備します。
init_db()


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/<path:filename>")
def files(filename):
    # DB・Pythonコード・Git情報を公開しないようにします。
    if filename not in {"index.html", "style.css", "script.js"}:
        abort(404)
    return send_from_directory(BASE_DIR, filename)


@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(status="error", message="JSON形式で送信してください。"), 400

    name = data.get("name")
    message = data.get("message")
    if not isinstance(name, str) or not isinstance(message, str):
        return jsonify(status="error", message="名前とお問い合わせ内容を文字列で送信してください。"), 400

    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            "INSERT INTO contacts (name, message) VALUES (?, ?)",
            (name, message)
        )

        conn.commit()

    return jsonify({
        "status": "success",
        "message": f"{name}さん、お問い合わせを保存しました！"
    })


if __name__ == "__main__":
    # ローカル勉強用。本番はGunicornを使います。
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")

