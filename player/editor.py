import chess.svg

import board
import agent
import database
import database.openings
import opening

from .openingPlayer import OpeningPlayer

class Editor(OpeningPlayer):
    
    def __init__(self, board: board.ChessBoard, op : opening.Opening):
        
        whiteAgent = agent.EditorOpeningAgent(op)
        blackAgent = whiteAgent
        
        OpeningPlayer.__init__(self, board, whiteAgent, blackAgent, op)
        
        self.root.bind("<<MoveProcessedBySuperPlayer>>", self.push, add=True)
        self.root.bind("<Delete>", self.delete)
        self.root.bind("<Control-s>", self.save)
        self.root.bind("<w>", self.write_annotation)
    
    def push(self, event):
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
    
    def write_annotation(self, event):
        moves = self.board.board.move_stack
        self.opening.line(moves)
        
        annotation = []
        
        for arrow in self.board.arrow_coords:
            start = arrow.head
            end = arrow.tail
            annotationArrow = chess.svg.Arrow(end, start, color="green")
            annotation.append(annotationArrow)
        
        self.opening.cursor.arrows_annotations = annotation
        self.display_annotation(event)
    
    def save(self, event):
        database.openings.save(self.opening, True)
        print("Opening saved")