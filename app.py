from flask import Flask, abort, jsonify, request, Response
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

STORAGE_FILE = "chatizens.db"


@app.before_first_request
def create_database_table():
    chatizen_storage = sqlite3.connect("chatizens.db")
    chatizen_storage.row_factory = sqlite3.Row
    c = chatizen_storage.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS chatizens (nick TEXT NOT NULL, lat REAL NOT NULL, lon REAL NOT NULL)")
    chatizen_storage.commit()
    c.close()


@app.route("/api/chatizen", methods=["GET"])
def get_all_chatizens():
    if request.cookies.get("password", "") != "sadmcasldkfjsdclasdkcmascdmklasdm":
        return Response(status=401)
    chatizen_storage = sqlite3.connect("chatizens.db")
    chatizen_storage.row_factory = sqlite3.Row
    c = chatizen_storage.cursor()
    rows = c.execute("SELECT * FROM chatizens").fetchall()
    ret = []
    for row in rows:
        ret.append(dict(row))
    c.close()
    chatizen_storage.close()
    return jsonify(ret)


@app.route("/api/chatizen/<nick>", methods=["GET"])
def get_chatizen(nick):
    if request.cookies.get("password", "") != "sadmcasldkfjsdclasdkcmascdmklasdm":
        return Response(status=401)
    chatizen_storage = sqlite3.connect("chatizens.db")
    chatizen_storage.row_factory = sqlite3.Row
    c = chatizen_storage.cursor()
    row = c.execute("SELECT * FROM chatizens WHERE nick = ?", (nick,))
    row = row.fetchone()
    c.close()
    chatizen_storage.close()
    if row is None:
        abort(404)
    else:
        return jsonify(dict(row))


@app.route("/api/chatizen/<nick>", methods=["POST"])
def add_chatizen(nick):
    chatizen_storage = sqlite3.connect("chatizens.db")
    chatizen_storage.row_factory = sqlite3.Row
    chatizen_data = dict(request.form)
    if "lat" not in chatizen_data or "lon" not in chatizen_data:
        abort(400)
    c = chatizen_storage.cursor()
    c.execute("INSERT INTO chatizens VALUES (?,?,?)", (nick, chatizen_data["lat"], chatizen_data["lon"]))
    chatizen_storage.commit()
    c.close()
    chatizen_storage.close()
    return Response(status=204)


@app.route("/api/chatizen/<nick>", methods=["DELETE"])
def delete_chatizen(nick):
    chatizen_storage = sqlite3.connect("chatizens.db")
    chatizen_storage.row_factory = sqlite3.Row
    c = chatizen_storage.cursor()
    row = c.execute("SELECT * FROM chatizens WHERE nick = ?", (nick,))
    row = row.fetchone()
    if row is None:
        c.close()
        chatizen_storage.close()
        abort(404)
    else:
        c.execute("DELETE FROM chatizens WHERE nick = ?", (nick,))
        chatizen_storage.commit()
        c.close()
        chatizen_storage.close()
        return Response(status=204)
