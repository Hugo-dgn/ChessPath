import utils

from .superAgent import Agent

class PgnAgent(Agent):
    
    def __init__(self, pgn):
        Agent.__init__(self)
        self.pgn = pgn
    
    def is_possible_action(self, board, move):
        moves = self.possible_actions(board)
        return move in moves
    
    def act(self, board, forwardCall):
        if not forwardCall:
            return None
        possible_actions = self.possible_actions(board)
        if len(possible_actions) == 0:
            return None
        else:
            return possible_actions[0]
    
    def possible_actions(self, board):
        node = self.pgn.game()
        move_stack = board.move_stack
        flag1 = True
        for move in move_stack:
            flag2 = False
            for child in node.variations:
                if move == child.move:
                    node = child
                    flag2 = True
                    break
            if not flag2:
                flag1 = False
                break
        if flag1:
            return [child.move for child in node.variations]
        else:
            return []
