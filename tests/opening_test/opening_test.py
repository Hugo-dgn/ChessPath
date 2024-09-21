import chess

import opening
import utils

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
    
    assert node.get_position() == utils.get_position(board), "The push method is not working."

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
    assert node.get_position() == utils.get_position(board), "The pop method is not working."

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
    assert node.get_position() == utils.get_position(board), "The back method is not working."

def test_move():
    op = opening.Opening("Ruy Lopez", chess.WHITE, opening.Node())
    board = chess.Board()
    move1 = chess.Move.from_uci("e2e4")
    move2 = chess.Move.from_uci("e7e5")
    
    op.push(move1)
    op.push(move2)
    
    board.push(move1)
    board.push(move2)
    
    leaf = op.cursor
    
    move3 = chess.Move.from_uci("g1f3")
    
    flag = op.move(move3)
    assert not flag, "The move method is not working."
    assert leaf.get_position() == utils.get_position(board), "The move method is not working."
    op.push(move3)
    board.push(move3)
    
    op.back()
    flag = op.move(move3)
    assert flag, "The move method is not working."
    
    node = op.cursor
    
    assert flag, "The move method is not working."
    assert node.get_position() == utils.get_position(board), "The move method is not working."

def test_eq():
    tree = opening.Node()
    op1 = opening.Opening("Ruy Lopez", chess.WHITE, tree)
    op2 = opening.Opening("Ruy Lopez", chess.WHITE, tree)
    
    move1 = chess.Move.from_uci("e2e4")
    move2 = chess.Move.from_uci("e7e5")
    
    
    op1.push(move1)
    op1.push(move2)
    
    op2.push(move1)
    op2.push(move2)
    
    assert op1 == op2, "The __eq__ method is not working."
    
    tree = opening.Node()
    op1 = opening.Opening("Ruy Lopez", chess.WHITE, tree)
    op2 = opening.Opening("Ruy Lopez", chess.WHITE, tree)
    
    move1 = chess.Move.from_uci("e2e4")
    move2 = chess.Move.from_uci("e7e5")
    move3 = chess.Move.from_uci("e7e6")
    
    op1.push(move1)
    op1.push(move2)
    
    op2.push(move1)
    op2.push(move3)
    
    assert not op1 != op2, "The __eq__ method is not working."
    
    tree = opening.Node()
    op1 = opening.Opening("Ruy Lopez", chess.WHITE, tree)
    op2 = opening.Opening("Ruy Lopez", chess.WHITE, tree)
    
    move1 = chess.Move.from_uci("e2e4")
    move2 = chess.Move.from_uci("e7e5")
    move3 = chess.Move.from_uci("e7e6")
    
    op1.push(move1)
    op1.push(move2)
    
    op2.push(move1)
    op2.push(move2)
    op2.root()
    op2.push(move1)
    op2.push(move3)
    
    assert not op1 != op2, "The __eq__ method is not working."
    assert not op2 != op1, "The __eq__ method is not working."
