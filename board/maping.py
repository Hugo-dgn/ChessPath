def get_square_pos(n_square, square_size, isfliped, center=False):
        x = (n_square%8)*square_size
        y = (7 - n_square//8)*square_size
        if isfliped:
            x = 7*square_size-x
            y = 7*square_size-y
        if center:
            x += square_size//2
            y += square_size//2
        return x, y

def get_square_from_click(x, y, case_size, isfliped):
    n = x//case_size + (7-y//case_size)*8
    if isfliped:
        n = 63 - n
    return n