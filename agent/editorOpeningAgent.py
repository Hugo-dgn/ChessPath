from .humanOpeningAgent import HumanOpeningAgent

class EditorOpeningAgent(HumanOpeningAgent):
    
    def __init__(self, opening):
        HumanOpeningAgent.__init__(self, opening)

    def is_possible_action(self, board, move):
        return True