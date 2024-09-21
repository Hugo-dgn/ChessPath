import chess

def get_position(board : chess.Board) -> str:
    return board.fen().split("-")[0]