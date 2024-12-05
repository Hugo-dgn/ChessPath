import time

import agent.humanTrainOpeningAgent
import board
import agent

from .openingPlayer import OpeningPlayer

class TrainPlayer(OpeningPlayer):
    
    def __init__(self, board: board.ChessBoard, openingName : str, color : bool, load = True):
        OpeningPlayer.__init__(self, board, openingName, color, load)
    
        self.color = color
        self.edit_mode = False
        self.anchor_fen = None

        self.root.bind("<<MoveConfirmation>>", self.update_success_rate)
        self.root.bind("<<Reset>>", self.move_on_reset)
        
        if self.color:
            self.whiteAgent = agent.HumanTrainOpeningAgent(self.opening)
            self.blackAgent = agent.TrainOpeningAgent(self.opening)
        else:
            self.whiteAgent = agent.TrainOpeningAgent(self.opening)
            self.blackAgent = agent.HumanTrainOpeningAgent(self.opening)
    
    def set_trained_color(self, color):
        self.color = color
        if color:
            self.whiteAgent = agent.HumanTrainOpeningAgent(self.opening)
            self.blackAgent = agent.TrainOpeningAgent(self.opening)
        else:
            self.whiteAgent = agent.TrainOpeningAgent(self.opening)
            self.blackAgent = agent.HumanTrainOpeningAgent(self.opening)
    
    def update_success_rate(self, event):
        flag1, flag2 = self.forward_draw(event)
        if len(self.board.board.move_stack) == 0:
            return flag1, flag2
        last_move = self.board.board.peek()
        self.opening.root()
        for move in self.board.board.move_stack[:-1]:
            self.opening.push(move)
        node = self.opening.cursor
        if not flag1:
            for link in node.children:
                link.visits += 1
        else:
            for link in node.children:
                if link.move == last_move:
                    link.visits += 1
                    link.successes += 1
        return flag1, flag2
    
    def move_on_reset(self, event):
        if not self.color:
            self.forward(event)