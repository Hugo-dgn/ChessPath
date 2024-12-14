class Agent:
    
    def __init__(self, isHuman):
        self.isHuman = isHuman
    
    def act(self, board, forwardCall):
        pass
    
    def possible_actions(self, board):
        return [move for move in board.legal_moves]

    def is_possible_action(self, board, move):
        return True