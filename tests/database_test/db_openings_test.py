import os

import chess

import database
import opening

OPENING_TEST_FILE = 'database/openings_test.db'

def overwrite_db_file():
    database.openings.opDatabase.OPENING_FILE = OPENING_TEST_FILE

def delete_db_file():
    os.remove(OPENING_TEST_FILE)

def test_save_db_opening():
    try:
        overwrite_db_file()
        tree = opening.Node()
        op = opening.Opening("test", chess.WHITE, tree)
        database.openings.save(op)
        delete_db_file()
    except Exception as e:
        delete_db_file()
        raise e

def test_load_db_opening():
    try:
        overwrite_db_file()
        op = opening.Opening("Ruy Lopez", chess.WHITE, opening.Node())
        board = chess.Board()
        
        move1 = chess.Move.from_uci("e2e4")
        move2 = chess.Move.from_uci("e7e5")
        
        op.push(move1)
        op.push(move2)
        
        board.push(move1)
        board.push(move2)
        
        database.openings.save(op)
        
        op_load = database.openings.load("Ruy Lopez", chess.WHITE)
        
        assert op == op_load, "The load method is not working."
        delete_db_file()
    except Exception as e:
        delete_db_file()
        raise e