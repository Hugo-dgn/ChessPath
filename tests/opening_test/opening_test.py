import chess

import opening

def test_push():
    op = opening.Opening("Ruy Lopez", chess.WHITE, opening.Node())
    board = chess.Board()
    
    move1 = chess.Move.from_uci("e2e4")
    move2 = chess.Move.from_uci("e7e5")
    
    op.push(move1)
    op.push(move2)
    
    board.push(move1)
    board.push(move2)
    
    node = op.cursor
    
    assert node.get_position() == board.fen().split("-")[0], "The push method is not working."

def test_pop():
    op = opening.Opening("Ruy Lopez", chess.WHITE, opening.Node())
    board = chess.Board()
    
    move1 = chess.Move.from_uci("e2e4")
    move2 = chess.Move.from_uci("e7e5")
    
    op.push(move1)
    op.push(move2)
    
    board.push(move1)
    board.push(move2)
    
    leaf = op.cursor
    
    op.pop()
    board.pop()
    
    node = op.cursor
    
    assert not node.is_child(leaf), "The pop method is not working."
    assert node.get_position() == board.fen().split("-")[0], "The pop method is not working."

def test_back():
    op = opening.Opening("Ruy Lopez", chess.WHITE, opening.Node())
    board = chess.Board()
    
    move1 = chess.Move.from_uci("e2e4")
    move2 = chess.Move.from_uci("e7e5")
    
    op.push(move1)
    op.push(move2)
    
    board.push(move1)
    board.push(move2)
    
    leaf = op.cursor
    
    op.back()
    board.pop()
    
    node = op.cursor
    
    assert node.is_child(leaf), "The back method is not working."
    assert node.get_position() == board.fen().split("-")[0], "The back method is not working."