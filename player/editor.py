import board
import agent
import database
import database.openings

from .openingPlayer import OpeningPlayer

class Editor(OpeningPlayer):
    
    def __init__(self, board: board.ChessBoard, openingName : str, color : bool):
        OpeningPlayer.__init__(self, board, openingName, color)
        self.root.bind("<<MoveConfirmation>>", self.push)
        self.root.bind("<Delete>", self.delete)
        
        self.whiteAgent = agent.EditorOpeningAgent(self.opening)
        self.blackAgent = self.whiteAgent
    
    def push(self, event):
        self.show_moves_if_persistent(event)
        self.opening.root()
        for move in self.board.board.move_stack:
            self.opening.push(move)
    
    def delete(self, event):
        if len(self.board.board.move_stack) == 0:
            return
        self.opening.root()
        for move in self.board.board.move_stack:
            self.opening.push(move)
        self.opening.pop()
        self.back(event)