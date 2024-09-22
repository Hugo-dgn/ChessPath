import opening as op

from .openingAgent import OpeningAgent

class TrainOpeningAgent(OpeningAgent):
    
    def __init__(self, opening):
        OpeningAgent.__init__(self, opening)
        self.set_score_function(op.successRateScore)