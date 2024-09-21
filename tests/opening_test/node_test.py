import chess

import opening
import utils
def test_node_eq():
    root1 = opening.Node()
    root2 = opening.Node()
    
    move1 = chess.Move.from_uci("e2e4")
    move2 = chess.Move.from_uci("e2e4")
    
    root1.add_child(move1)
    root2.add_child(move2)
    
    assert root1 == root2, "The __eq__ method is not working."
    
    root1 = opening.Node()
    root2 = opening.Node()
    
    move1 = chess.Move.from_uci("e2e3")
    move2 = chess.Move.from_uci("e2e4")
    
    root1.add_child(move1)
    root2.add_child(move2)
    
    assert root1 == root2, "The __eq__ method is not working."

def test_node_add_child():
    root = opening.Node()
    
    move1 = chess.Move.from_uci("e2e4")
    move2 = chess.Move.from_uci("e2e4")
    
    root.add_child(move1)
    root.add_child(move2)
    
    assert len(root.children) == 1, "The add_child allows for duplicate children."

def test_get_position():
    move1 = chess.Move.from_uci("e2e4")
    move2 = chess.Move.from_uci("e7e5")
    
    root = opening.Node()
    leaf1 = root.add_child(move1)
    leaf2 = leaf1.add_child(move2)
    
    position = leaf2.get_position()
    
    board = chess.Board()
    board.push(move1)
    board.push(move2)
    true_position = utils.get_position(board)
    
    assert position == true_position, "The get_position method is not working."

def test_twin():
    move1 = chess.Move.from_uci("e2e4")
    move2 = chess.Move.from_uci("e7e5")
    
    move3 = chess.Move.from_uci("e2e3")
    move4 = chess.Move.from_uci("e7e6")
    move5 = chess.Move.from_uci("e3e4")
    move6 = chess.Move.from_uci("e6e5")
    
       
    root = opening.Node()
    leaf1 = root.add_child(move1)
    leaf2 = leaf1.add_child(move2)
    
    leaf3 = root.add_child(move3)
    leaf4 = leaf3.add_child(move4)
    leaf5 = leaf4.add_child(move5)
    leaf6 = leaf5.add_child(move6)
    
    assert leaf2 is leaf6, "The _find_twin method is not working."

def test_delete_child():
    move1 = chess.Move.from_uci("e2e4")
    move2 = chess.Move.from_uci("e7e5")
    
    root = opening.Node()
    leaf1 = root.add_child(move1)
    leaf2 = leaf1.add_child(move2)
    
    leaf1.delete_child(move2)
    
    assert len(leaf1.children) == 0, "The delete_child method is not working."
    assert len(leaf2.parents) == 0, "The delete_child method is not working."

def test_back():
    move1 = chess.Move.from_uci("e2e4")
    move2 = chess.Move.from_uci("e7e5")
    
    root = opening.Node()
    leaf1 = root.add_child(move1)
    leaf2 = leaf1.add_child(move2)
    
    assert leaf2.back(move2) is leaf1, "The back method is not working."