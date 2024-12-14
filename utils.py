import chess

import database

def get_position(board : chess.Board) -> str:
    split = board.fen().split()
    return " ".join(split[:4])

def get_openings():
    ops = database.openings.openings()
    
    black = []
    white = []
    for name, color in ops:
        op = database.openings.load(name, color)
        if color:
            white.append(op)
        else:
            black.append(op)
            
    return white, black