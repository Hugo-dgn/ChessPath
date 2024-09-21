import random

from .superAgent import Agent

class OpeningAgent(Agent):
    
    def __init__(self, opening):
        lock = True
        Agent.__init__(self, lock)
        self.opening = opening
    
    def act(self, board):
        stack = board.move_stack
        self.opening.root()
        for move in stack:
            flag = self.opening.move(move)
            if not flag:
                return None

        next_moves = self.opening.next()
        if len(next_moves) == 0:
            return None
        move = random.choice(next_moves)
        return move