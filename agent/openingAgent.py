import random

from .superAgent import Agent

class OpeningAgent(Agent):
    
    def __init__(self, opening):
        Agent.__init__(self)
        self.opening = opening
    
    def is_possible_action(self, board, move):
        moves = self.possible_actions(board)
        return move in moves
    
    def act(self, board):
        next_moves = self.possible_actions(board)
        if len(next_moves) == 0:
            return None
        move = random.choice(next_moves)
        return move
    
    def possible_actions(self, board):
        stack = board.move_stack
        self.opening.root()
        for move in stack:
            flag = self.opening.move(move)
            if not flag:
                return []

        return self.opening.next()