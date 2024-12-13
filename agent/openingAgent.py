import random

import opening as op
import utils

from .superAgent import Agent

class OpeningAgent(Agent):
    
    def __init__(self, opening):
        Agent.__init__(self)
        self.opening = opening
        self.score_function = op.depthScore
    
    def set_score_function(self, score_function):
        self.score_function = score_function
    
    def is_possible_action(self, board, move):
        moves = self.possible_actions(board)
        return move in moves
    
    def act(self, board, forwardCall):
        next_moves = self.possible_actions(board)
        if len(next_moves) == 0:
            return None
        if forwardCall:
            node = self.opening.cursor
            scores = self.score_function(node)
            move = max(scores, key=lambda x: x[0])[1]
        else:
            move = random.choice(next_moves)
        return move
    
    def possible_actions(self, board):
        position = utils.get_position(board)
        if position in self.opening.lookup:
            node = self.opening.lookup[position]
            self.opening.cursor = node
            return node.get_moves()
        else:
            return []