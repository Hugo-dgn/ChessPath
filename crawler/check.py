from tqdm.auto import tqdm
import copy

import database
import database.openings

def fromPGN(pgns, player_name, max_deviation):
    ops = database.openings.openings()
    
    white_mistakes = []
    black_mistakes = []
    
    black = []
    white = []
    for name, color in ops:
        if color:
            white.append(database.openings.load(name, color))
        else:
            black.append(database.openings.load(name, color))
    
    for pgn in tqdm(pgns):
        if pgn.headers["White"].lower() == player_name.lower():
            color = 1
            repertoire = [copy.deepcopy(op) for op in white]
        elif pgn.headers["Black"].lower() == player_name.lower():
            color = 0
            repertoire = [copy.deepcopy(op) for op in black]
        else:
            raise ValueError("Player name not found in PGN")
        
        deviation_op = [0 for _ in range(len(repertoire))]
        
        for i, move in enumerate(pgn.mainline_moves()):
            _ = 1
            for j, op in enumerate(repertoire):
                if deviation_op[j] > max_deviation:
                    continue
                if (i+1) % 2 == color:
                    possible_moves = op.cursor.get_moves()
                    flag = move in possible_moves
                    op.push(move)
                    if not flag:
                        deviation_op[j] += 1
                    if not flag and len(possible_moves) > 0:
                        move = i//2 + 1
                        add_mistake(op, pgn, move, color, white_mistakes, black_mistakes)
                else:
                    flag = move in op.cursor.get_moves()
                    if not flag:
                        deviation_op[j] += 1
                    try:
                        op.push(move)
                    except:
                        _ = 1
    
    return white_mistakes, black_mistakes

def add_mistake(op, pgn, move, color, white_mistakes, black_mistakes):
    if color:
        white_mistakes.append((op.name, move, pgn))
    else:
        black_mistakes.append((op.name, move, pgn))