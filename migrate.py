import sqlite3


def migrate():
    conn = sqlite3.connect('database.sqlite')

    c = conn.cursor()

    c.execute(
        'CREATE TABLE "jobs" ("id" varchar,"created_at" datetime,"processed" int, "url" varchar, "dir" varchar, "filename" varchar, PRIMARY KEY (id));')


migrate()
