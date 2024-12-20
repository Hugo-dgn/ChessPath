import yaml
import pandas as pd
import os

import opening
import database.utils as utils

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
DATABASE_FILE = config['database']

def list_tables():
    exists = os.path.exists(DATABASE_FILE)
    if not exists:
        raise FileNotFoundError(f"Database file {DATABASE_FILE} not found")
    conn = utils.create_connection(DATABASE_FILE)
    rows = utils.list_table(conn)
    return rows

def reset():
    conn = utils.create_connection(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS openings")
    cur.execute("CREATE TABLE openings ( color BOOL, name STRING, pgn STRING, PRIMARY KEY (color, name));")
    conn.commit()
    conn.close()

def table(name):
    tables = list_tables()
    if (name,) not in tables:
        assert False, f"Table {name} not found"
    conn = utils.create_connection(DATABASE_FILE)
    query = f"SELECT * FROM {name}"
    df = pd.read_sql_query(query, conn)
    return df

def openings():
    conn = utils.create_connection(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("SELECT name, color FROM openings")
    op = cur.fetchall()
    return op

def set_pgn(name, color, pgn):
    conn = utils.create_connection(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("UPDATE openings SET pgn = ? WHERE color = ? AND name = ?", (pgn, color, name))
    conn.commit()
    
def get_pgn(name, color):
    conn = utils.create_connection(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("SELECT pgn FROM openings WHERE name = ? AND color = ?", (name, color))
    pgn = cur.fetchone()[0]
    return pgn
    

def save(opening, overwrite=False):
    tables = list_tables()
    if ('openings',) not in tables:
        reset()
        
    name = opening.name
    color = opening.color
    pgn = opening.get_pgn()
    
    conn = utils.create_connection(DATABASE_FILE)
    cur = conn.cursor()
    if overwrite:
        cur.execute("UPDATE openings SET pgn = ? WHERE color = ? AND name = ?", (pgn, color, name))
        if cur.rowcount == 0:
            cur.execute("INSERT INTO openings (name, color, pgn) VALUES (?, ?, ?)", (name, color, pgn))
    else:
        cur.execute("SELECT * FROM openings WHERE name = ? AND color = ?", (name, color))
        if cur.fetchone() is not None:
            print("Opening already exists")
            return
        cur.execute("INSERT INTO openings (name, color, pgn) VALUES (?, ?, ?)", (name, color, pgn))
    cur.close()
    conn.commit()

def delete(name, color):
    conn = utils.create_connection(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM openings WHERE name = ? AND color = ?", (name, color))
    conn.commit()


def load(name, color):
    pgn = get_pgn(name, color)
    if pgn is None:
        return None
    op = opening.from_pgn(name, color, pgn)
    return op