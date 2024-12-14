import chess
from tqdm.auto import tqdm

import agent
import utils

def fromPGN(pgns, player_name):
    
    mistakes = {}
    
    white, black = utils.get_openings()

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
        multiAgent = agent.MultiOpeningAgent(repertoire, isHuman=False)
        for move in pgn.mainline_moves():
            moves = multiAgent.possible_actions(board)
            if len(moves) > 0 and board.turn == color:
                if move not in moves:
                    position = utils.get_position(board)
                    if position not in mistakes:
                        mistakes[position] = {"n" : 0, "moves" : [], "staks" : []}
                    mistakes[position]["n"] += 1
                    mistakes[position]["moves"].append(move)
                    mistakes[position]["staks"].append(board.move_stack.copy())
            board.push(move)
    return mistakes