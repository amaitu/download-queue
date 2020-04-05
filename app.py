from flask import Flask
from flask import request
import sqlite3

app = Flask(__name__)


@app.route("/downloads/all", methods=["GET"])
def get_all_downloads():
    # INSERT
    # INTO
    # "jobs"("id", "created_at", "processed", "url", "dir", "filename")
    # VALUES
    # ('7d2e4aaa-5901-46aa-82ad-8950e839078b', '2020-01-01 00:00:00', '0', 'https://sgbarker.com', 'lund', 'lund.csv');

    processed = None

    if request.args.get("processed") == "true":
        processed = "1"

    if request.args.get("processed") == "false":
        processed = "0"

    conn = sqlite3.connect("database.sqlite")
    c = conn.cursor()

    results = {}

    if processed is None:
        query = c.execute(
            "SELECT id, created_at, processed, url, dir, filename FROM jobs ORDER BY created_at DESC LIMIT 250"
        )
    else:
        print(processed)
        query = c.execute(
            "SELECT id, created_at, processed, url, dir, filename FROM jobs WHERE processed = ? ORDER BY created_at DESC LIMIT 250",
            processed,
        )

    for row in query:
        result_id = row[0]
        result = {
            "id": result_id,
            "created_at": row[1],
            "processed": row[2],
            "url": row[3],
            "dir": row[4],
            "filename": row[5],
        }

        results[result_id] = result

    return results


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
