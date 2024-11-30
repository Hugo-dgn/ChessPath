import time

import agent.humanTrainOpeningAgent
import board
import agent

from .openingPlayer import OpeningPlayer

class TrainPlayer(OpeningPlayer):
    
    def __init__(self, board: board.ChessBoard, openingName : str, color : bool):
        OpeningPlayer.__init__(self, board, openingName, color)
        
        if color == "w":
            self.whiteAgent = agent.HumanTrainOpeningAgent(self.opening)
            self.blackAgent = agent.TrainOpeningAgent(self.opening)
        else:
            self.whiteAgent = agent.TrainOpeningAgent(self.opening)
            self.blackAgent = agent.HumanTrainOpeningAgent(self.opening)
    
        self.color = color
        self.edit_mode = False
        self.anchor_fen = None

        self.root.bind("<<MoveConfirmation>>", self.update_success_rate)
        self.root.bind("<<Reset>>", self.move_on_reset)
        self.root.bind("<t>", self.toggle)
        self.root.bind("<a>", self.anchor)
        self.root.bind("<A>", self.go_to_anchor)
    
    def update_success_rate(self, event):
        if len(self.board.board.move_stack) == 0:
            return
        last_move = self.board.board.peek()
        self.opening.root()
        for move in self.board.board.move_stack[:-1]:
            self.opening.push(move)
        node = self.opening.cursor
        flag1, flag2 = self.move(event, False)
        if not flag1:
            for link in node.children:
                link.visits += 1
        else:
            for link in node.children:
                if link.move == last_move:
                    link.visits += 1
                    link.successes += 1
    
    def move_on_reset(self, event):
        if not self.color:
            self.forward(event)
    
    def toggle(self, event):
        if self.color:
            if self.edit_mode:
                self.blackAgent = agent.TrainOpeningAgent(self.opening)
            else:
                self.blackAgent = agent.HumanTrainOpeningAgent(self.opening)
        else:
            if self.edit_mode:
                self.whiteAgent = agent.TrainOpeningAgent(self.opening)
            else:
                self.whiteAgent = agent.HumanTrainOpeningAgent(self.opening)

        self.edit_mode = not self.edit_mode
    
    def anchor(self, event):
        self.anchor_fen = self.board.board.fen()
        
    def go_to_anchor(self, event):
        if self.anchor_fen is None:
            return
        self.board.reset(self.anchor_fen)