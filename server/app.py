from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Endpoint para listar os dados
@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, sensor, value, unit, timestamp, location, status, valid
        FROM sensor_data
        ORDER BY timestamp DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    data = [
        {
            "id": row[0],
            "sensor": row[1],
            "value": row[2],
            "unit": row[3],
            "timestamp": row[4],
            "location": row[5],
            "status": row[6],
            "valid": bool(row[7])
        }
        for row in rows
    ]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
