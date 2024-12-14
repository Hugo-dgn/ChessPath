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
        flag = move in moves
        node = self.get_node(board)
        if node is not None:
            node.visits += 1
            node.success += int(flag)
        return flag
    
    def act(self, board, forwardCall):
        if self.isHuman:
            move = None
        else:
            position = utils.get_position(board)
            if position in self.opening.lookup:
                node = self.opening.lookup[position]
                scores = self.score_function(node)
                if len(scores) == 0:
                    move = None
                elif forwardCall:
                    move = max(scores, key=lambda x: x[0])[1]
                else:
                    moves = [score[1] for score in scores]
                    y = [score[0] for score in scores]
                    s = sum(y)
                    p = [x/s for x in y]
                    move = random.choices(moves, p)[0]
            else:
                move = None
        return move
    
    def get_arrows_annotations(self, board):
        position = utils.get_position(board)
        if position in self.opening.lookup:
            node = self.opening.lookup[position]
            return node.arrows_annotations
        else:
            return []
    def get_node(self, board):
        position = utils.get_position(board)
        if position in self.opening.lookup:
            return self.opening.lookup[position]
        else:
            return None
    
    def possible_actions(self, board):
        node = self.get_node(board)
        if node is None:
            return []
        self.opening.cursor = node
        return node.get_moves()