import board
import agent
import database
import opening as op

from .superplayer import Player

import time

class OpeningPlayer(Player):
    
    def __init__(self, board: board.ChessBoard, openingName : str, color : bool):
        self.opening = database.openings.load(openingName, color)
        if self.opening is None:
            print("Opening not found, creating new opening")
            self.opening = op.Opening(openingName, color, op.Node())
        
        whiteAgent = agent.HumanOpeningAgent(self.opening)
        blackAgent = whiteAgent
        
        Player.__init__(self, board, whiteAgent, blackAgent)
        
        self.persistent_show_moves = False
        self.show_annotation = False
        
        self.root.bind("<S>", self.show_moves_persistent)
        self.root.bind("<s>", self.show_moves_non_persistent)
        self.root.bind("<c>", self.clear)
        self.root.bind("<W>", self._display_annotation)
        self.root.bind("<space>", self.hint_moves)
        self.root.bind("<<MoveConfirmation>>", self.forward_draw)
        self.root.bind("<<MoveBack>>", self.backward_draw)

    def show_moves(self, persistent, fill=None):
        moves = self.whiteAgent.possible_actions(self.board.board)
        for move in moves:
            start = move.from_square
            end = move.to_square
            self.board.arrow(start, end, persistent, fill)
    
    def show_moves_non_persistent(self, event):
        self.show_moves(persistent=False, fill="blue")
    
    def show_moves_persistent(self, event):
        self.persistent_show_moves = not self.persistent_show_moves
        self.show_moves(self.persistent_show_moves)
        
    def forward_draw(self, event):
        self.board.clear()
        if self.show_annotation:
            self.display_annotation(event)
        self.move(event, False)
        if self.persistent_show_moves:
            self.show_moves(True)
        
    
    def backward_draw(self, event):
        self.board.clear()
        if self.show_annotation:
            self.display_annotation(event)
        if self.persistent_show_moves:
            self.show_moves(True)
        
    
    def clear(self, event):
        self.board.clear()
        self.persistent_show_moves = False
    
    def hint_moves(self, event):
        moves = self.whiteAgent.possible_actions(self.board.board)
        for move in moves:
            start = move.from_square
            self.board.highlight(start)
        
    def _display_annotation(self, event):
        self.show_annotation = not self.show_annotation
        self.display_annotation(event)
    
    def display_annotation(self, event):
        moves = self.board.board.move_stack
        cursor = self.opening.line(moves)
        
        arrow_coords = cursor.arrows_annotations
        highlight_coords = cursor.highlight_annotations
        
        
        for arrow_coord in arrow_coords:
            self.board.arrow(arrow_coord[0], arrow_coord[1], persistent=False, fill="green")
        
        for highlight_coord in highlight_coords:
            self.board.highlight(highlight_coord, fill="green")