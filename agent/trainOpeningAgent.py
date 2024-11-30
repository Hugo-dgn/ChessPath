import opening as op

from .openingAgent import OpeningAgent

class TrainOpeningAgent(OpeningAgent):
    
    def __init__(self, opening):
        OpeningAgent.__init__(self, opening)
        self.set_score_function(op.successRateScore)
    
    def act(self, board, forwardCall):
        next_moves = self.possible_actions(board)
        if len(next_moves) == 0:
            return None
        node = self.opening.cursor
        move = self.score_function(node)
        return move