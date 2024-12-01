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
        self.root.bind("<Control-s>", self.save)
        self.root.bind("<w>", self.write_annotation)
        
        self.whiteAgent = agent.EditorOpeningAgent(self.opening)
        self.blackAgent = self.whiteAgent
    
    def push(self, event):
        self.opening.root()
        for move in self.board.board.move_stack:
            self.opening.push(move)
        self.forward_draw(event)
    
    def delete(self, event):
        if len(self.board.board.move_stack) == 0:
            return
        self.opening.root()
        for move in self.board.board.move_stack:
            self.opening.push(move)
        self.opening.pop()
        self.back(event)
    
    def write_annotation(self, event):
        moves = self.board.board.move_stack
        self.opening.line(moves)
        
        self.opening.cursor.arrows_annotations = [coord for coord in self.board.arrow_coords]
        self.opening.cursor.highlight_annotations = [coord for coord in self.board.highlight_coords]
        self.display_annotation(event)
    
    def save(self, event):
        database.openings.save(self.opening, True)
        print("Opening saved")