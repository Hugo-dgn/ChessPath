import numpy as np

import opening as op

from .openingAgent import OpeningAgent

class TrainOpeningAgent(OpeningAgent):
    
    def __init__(self, opening):
        OpeningAgent.__init__(self, opening)
        self.set_score_function(op.agrregationScore)
    
    def act(self, board, forwardCall):
        next_moves = self.possible_actions(board)
        if len(next_moves) == 0:
            return None
        node = self.opening.cursor
        scores = self.score_function(node)
        wheigths = np.array([score[0] for score in scores])
        moves = [score[1] for score in scores]
        wheigths = wheigths / wheigths.sum()
        move = np.random.choice(moves, p=wheigths)
        return move