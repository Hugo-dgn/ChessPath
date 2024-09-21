from .superAgent import Agent

class OpeningAgent(Agent):
    
    def __init__(self, lock, opening):
        Agent.__init__(self, lock)
        self.opening = opening
    
    def act(self, board):
        stack = board.move_stack()
        for move in stack:
            flag = self.opening.move(move)
            if not flag:
                return None