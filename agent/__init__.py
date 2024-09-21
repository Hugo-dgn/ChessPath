from .superAgent import Agent

import utils as _utils

class OpeningsAgent(Agent):
    def __init__(self, opening):
        self.opening = opening
        lock = opening.color
        Agent.__init__(self, lock)
    
    def act(self, board):
        if not _utils.get_position(board) == self.opening.cursor.get_position():
            self.opening.root()