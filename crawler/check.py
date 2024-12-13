import chess
from tqdm.auto import tqdm
import copy

import database
import utils

def fromPGN(pgns, player_name):
    ops = database.openings.openings()
    
    white_mistakes = []
    black_mistakes = []
    
    black = []
    white = []
    for name, color in ops:
        op = database.openings.load(name, color)
        if color:
            white.append(op)
        else:
            black.append(op)
    
    for pgn in tqdm(pgns):
        if pgn.headers["White"].lower() == player_name.lower():
            color = 1
            repertoire = white
        elif pgn.headers["Black"].lower() == player_name.lower():
            color = 0
            repertoire = black
        else:
            raise ValueError("Player name not found in PGN")
        
        board = chess.Board()
        for move in pgn.mainline_moves():
            position = utils.get_position(board)
            for op in repertoire:
                if board.turn == color:
                    if position in op.lookup:
                        node = op.lookup[position]
                        moves = node.get_moves()
                        if move not in moves and len(moves) > 0:
                            add_mistake(op, node, pgn, board.fullmove_number, color, white_mistakes, black_mistakes)
            board.push(move)
    return white_mistakes, black_mistakes

def add_mistake(op, node, pgn, move, color, white_mistakes, black_mistakes):
    data = {'opening' : op, 'node' : node, 'pgn' : pgn, 'move' : move}
    if color:
        white_mistakes.append(data)
    else:
        black_mistakes.append(data)