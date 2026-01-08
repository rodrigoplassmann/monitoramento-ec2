from flask import Flask, request, jsonify
import pymysql, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

@app.route("/metrics", methods=["POST"])
def receive():
    data = request.json
    cursor = conn.cursor()
    cursor.execute(
	"INSERT INTO metrics (cpu, ram, disk) VALUES (%s,%s,%s)",
	(data["cpu"], data["ram"], data["disk"])
    )
    conn.commit()
    return jsonify({"status":"ok"})

@app.route("/metrics", methods=["GET"])
def read():
    cursor = conn.cursor()
    cursor.execute("SELECT cpu,ram,disk,created_at FROM metrics ORDER BY created_at DESC LIMIT 10")
    rows = cursor.fetchall()
    return jsonify(rows)

app.run(host="0.0.0.0", port=5000)
