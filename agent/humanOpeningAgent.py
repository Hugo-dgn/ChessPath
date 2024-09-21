from .openingAgent import OpeningAgent

class HumanOpeningAgent(OpeningAgent):
    
    def __init__(self, opening):
        OpeningAgent.__init__(self, opening)
    
    def act(self, board):
        return None