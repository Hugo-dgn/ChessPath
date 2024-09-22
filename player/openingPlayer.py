import board
import agent
import database
import opening as op

from .superplayer import Player

class OpeningPlayer(Player):
    
    def __init__(self, board: board.ChessBoard, openingName : str, color : bool):
        self.opening = database.openings.load(openingName, color)
        if self.opening is None:
            print("Opening not found, creating new opening")
            self.opening = op.Opening(openingName, color, op.Node())
        
        whiteAgent = agent.HumanOpeningAgent(self.opening)
        blackAgent = whiteAgent
        
        Player.__init__(self, board, whiteAgent, blackAgent)
        
        if not color:
            self.board.flip()
        
        self.persistent_show_moves = False
        
        self.root.bind("<S>", self.show_moves_persistent)
        self.root.bind("<s>", self.show_moves_non_persistent)
        self.root.bind("<c>", self.clear)
        self.root.bind("<Control-s>", self.save)
        self.root.bind("<space>", self.hint_moves)
        self.root.bind("<<MoveConfirmation>>", self.show_moves_if_persistent)
        self.root.bind("<<MoveBack>>", self.show_moves_if_persistent_back)

    def show_moves(self, persistent):
        moves = self.whiteAgent.possible_actions(self.board.board)
        for move in moves:
            start = move.from_square
            end = move.to_square
            self.board.arrow(start, end, persistent)
    
    def show_moves_non_persistent(self, event):
        self.show_moves(False)
    
    def show_moves_persistent(self, event):
        self.persistent_show_moves = True
        self.show_moves(True)
    
    def show_moves_if_persistent(self, event):
        self.move(event, False)
        self.board.clear()
        if self.persistent_show_moves:
            self.show_moves(True)
            
    def show_moves_if_persistent_back(self, event):
        self.board.clear()
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
    
    def save(self, event):
        database.openings.save(self.opening, True)