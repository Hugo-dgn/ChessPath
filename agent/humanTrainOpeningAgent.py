from .openingAgent import OpeningAgent

class HumanTrainOpeningAgent(OpeningAgent):
    
    def __init__(self, opening):
        OpeningAgent.__init__(self, opening)
        
    def act(self, board, forwardCall):
        return None