import chess

from agent import OpeningAgent
import opening

def test_act():
    op = opening.Opening("Ruy Lopez", chess.WHITE, opening.Node())
    board = chess.Board()
    
    move1 = chess.Move.from_uci("e2e4")
    move2 = chess.Move.from_uci("e7e5")
    
    op.push(move1)
    op.push(move2)
    
    board.push(move1)
    
    ag = OpeningAgent(op)
    assert ag.lock, "The lock attribute is True for the OpeningAgent, it should be False."
    
    move = ag.act(board)
    assert move == move2, "The act method is not working."
    
    board.push(move2)
    move = ag.act(board)
    assert move is None, "The act method is not working."
    
    