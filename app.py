import os
import sqlite3

import requests
from flask import Flask
from flask import request

app = Flask(__name__)


class Job:
    def __init__(
        self,
        uuid: str,
        created_at: str,
        processed: bool,
        url: str,
        directory: str,
        filename: str,
    ):
        self.uuid = uuid
        self.created_at = created_at
        self.processed = processed
        self.url = url
        self.directory = directory
        self.filename = filename


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


def get_next_job_in_queue():
    conn = sqlite3.connect("database.sqlite")
    c = conn.cursor()

    query = c.execute(
        "SELECT id, created_at, processed, url, dir, filename FROM jobs WHERE processed = ? ORDER BY created_at asc LIMIT 1",
        "0",
    )

    for row in query:
        result_id = row[0]

        job = Job(
            uuid=result_id,
            created_at=row[1],
            processed=row[2],
            url=row[3],
            directory=row[4],
            filename=row[5],
        )

        conn.close()
        return job


@app.route("/process", methods=["GET"])
def process():
    job = get_next_job_in_queue()

    if job is None:
        return "No jobs found."

    download_a_file(
        url=job.url, name=job.filename, directory=job.directory,
    )

    mark_job_as_complete(job=job)

    return "downloaded"


def mark_job_as_complete(job: Job) -> bool:
    try:
        conn = sqlite3.connect("database.sqlite")
        c = conn.cursor()

        c.execute("UPDATE JOBS SET processed = 1 WHERE ID = ?", (job.uuid,))

        conn.commit()
        conn.close()
    except Exception:
        return False

    return True


def download_a_file(url: str, name: str, directory: str):
    local_filename = "{}.{}".format(name, url.split(".")[-1])

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    os.makedirs(directory, exist_ok=True)
    os.replace(local_filename, "{}/{}".format(directory, local_filename))
    return local_filename


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
