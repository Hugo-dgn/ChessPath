import random

import opening as op
import utils

from .superAgent import Agent

class OpeningAgent(Agent):
    
    def __init__(self, opening, isHuman, lock=True):
        Agent.__init__(self, isHuman)
        self.opening = opening
        self.score_function = op.depthScore
        self.lock = lock
    
    def set_score_function(self, score_function):
        self.score_function = score_function
    
    def is_possible_action(self, board, move):
        if not self.lock:
            return True
        moves = self.possible_actions(board)
        return move in moves
    
    def act(self, board, forwardCall):
        if forwardCall:
            position = utils.get_position(board)
            if position in self.opening.lookup:
                node = self.opening.lookup[position]
                scores = self.score_function(node)
                move = max(scores, key=lambda x: x[0])[1]
            else:
                move = None
        elif self.isHuman:
            move = None
        else:
            next_moves = self.possible_actions(board)
            if len(next_moves) == 0:
                return None
            move = random.choice(next_moves)
        return move
    
    def get_arrows_annotations(self, board):
        position = utils.get_position(board)
        if position in self.opening.lookup:
            node = self.opening.lookup[position]
            return node.arrows_annotations
        else:
            return []
    
    def possible_actions(self, board):
        position = utils.get_position(board)
        if position in self.opening.lookup:
            node = self.opening.lookup[position]
            self.opening.cursor = node
            return node.get_moves()
        else:
            return []