class Node:
    
    def __init__(self, move):
        self.move = move
        self.children = []
        self.parents = []
        self.visits = 0
        self.successes = 0
    
    def add_child(self, child):
        child_move = self.get_child_move()
        if child.move not in child_move:
            self.children.append(child)
            child.parents.append(self)
    
    def get_child_move(self):
        moves = []
        for child in self.children:
            moves.append(child.move)
        return moves
        
    def __eq__(self, other):
        return self.move == other.move