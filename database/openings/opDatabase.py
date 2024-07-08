import pickle

import opening
import database.utils as utils

OPENING_FILE = 'database/openings.db'

def reset():
    conn = utils.create_connection(OPENING_FILE)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS openings")
    cur.execute("CREATE TABLE openings ( color BOOL, name STRING, tree BLOB, PRIMARY KEY (color, name));")
    conn.commit()
    conn.close()

def tables():
    conn = utils.create_connection(OPENING_FILE)
    rows = utils.list_table(conn)
    return rows

def openings():
    conn = utils.create_connection(OPENING_FILE)
    cur = conn.cursor()
    cur.execute("SELECT name FROM openings")
    names = cur.fetchall()
    return names
    

def save(opening):
    list_tables = tables()
    if ('openings',) not in list_tables:
        reset()
    name = opening.name
    color = opening.color
    tree = opening.tree
    
    conn = utils.create_connection(OPENING_FILE)
    cur = conn.cursor()
    serialized_tree = pickle.dumps(tree)
    cur.execute("INSERT INTO openings (name, color, tree) VALUES (?, ?, ?)", (name, color, serialized_tree))
    cur.close()
    conn.commit()

def load(name, color):
    conn = utils.create_connection(OPENING_FILE)
    cur = conn.cursor()
    cur.execute("SELECT tree FROM openings WHERE name = ? AND color = ?", (name, color))
    tree = cur.fetchone()
    if tree is None:
        return None
    tree = pickle.loads(tree[0])
    op = opening.Opening(name, color, tree)
    return op