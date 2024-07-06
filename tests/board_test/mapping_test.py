import board.mapping as mapping

def test_get_square_pos():
    n_quare = 0
    
    pos = mapping.get_square_pos(n_quare, 100, False)
    
    assert pos == (0, 700)
    
    pos = mapping.get_square_pos(n_quare, 100, True)
    
    assert pos == (700, 0)
    
    n_square = 10
    
    pos = mapping.get_square_pos(n_square, 100, False)
    
    assert pos == (200, 600)
    
    pos = mapping.get_square_pos(n_square, 100, True)
    
    assert pos == (500, 100)