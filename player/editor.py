import chess.svg

import board
import agent
import database
import database.openings
import opening
import utils

from .openingPlayer import OpeningPlayer

class Editor(OpeningPlayer):
    
    def __init__(self, board: board.ChessBoard, op : opening.Opening):
        self.opening = op
        
        whiteAgent = agent.OpeningAgent(op, isHuman=True, lock=False)
        blackAgent = whiteAgent
        openingAgent = agent.OpeningAgent(op, isHuman=False)
        
        OpeningPlayer.__init__(self, board, whiteAgent, blackAgent, openingAgent)
        
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
        position = utils.get_position(self.board.board)
        node = self.opening.lookup[position]
        
        annotation = []
        
        for arrow in self.board.arrow_coords:
            start = arrow.head
            end = arrow.tail
            annotationArrow = chess.svg.Arrow(end, start, color="green")
            annotation.append(annotationArrow)
        
        node.arrows_annotations = annotation
        self.display_annotation(event)
    
    def save(self, event):
        database.openings.save(self.opening, True)
        print("Opening saved")