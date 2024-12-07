import chess.svg

import board
import agent
import opening as op

from .superplayer import Player

class OpeningPlayer(Player):
    
    def __init__(self, board: board.ChessBoard, opening : op.Opening):
        self.opening = opening
        
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
        self.root.bind("<<MoveProcessedBySuperPlayer>>", self.forward_draw, add=True)
        self.root.bind("<<MoveBack>>", self.backward_draw)

    def show_moves(self, persistent):
        moves = self.whiteAgent.possible_actions(self.board.board)
        for move in moves:
            start = move.from_square
            end = move.to_square
            arrow = chess.svg.Arrow(end, start, color="blue")
            self.board.arrow(arrow, persistent=persistent)
    
    def show_moves_non_persistent(self, event):
        self.show_moves(persistent=False)
    
    def show_moves_persistent(self, event):
        self.persistent_show_moves = not self.persistent_show_moves
        self.show_moves(self.persistent_show_moves)
        
    def forward_draw(self, event):
        self.board.clear()
        if self.show_annotation:
            self.display_annotation(event)
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
        cursor, flag = self.opening.line(moves)
        
        if not flag:
            return
        
        arrows = cursor.arrows_annotations
        
        for arrow in arrows:
            self.board.arrow(arrow)