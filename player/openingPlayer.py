import board
import agent
import database
import database.openings

from .superplayer import Player

class OpeningPlayer(Player):
    
    def __init__(self, board: board.ChessBoard, openingName : str, color : bool):
        self.opening = database.openings.load(openingName, color)
        
        if color:
            whiteAgent = agent.HumanOpeningAgent(self.opening)
            blackAgent = agent.OpeningAgent(self.opening)
            self.human = whiteAgent
        else:
            whiteAgent = agent.OpeningAgent(self.opening)
            blackAgent = agent.HumanOpeningAgent(self.opening)
            self.human = blackAgent
        
        Player.__init__(self, board, whiteAgent, blackAgent)
        
        self.persistent_show_moves = False
        
        self.root.bind("<S>", self.show_moves_persistent)
        self.root.bind("<s>", self.show_moves_non_persistent)
        self.root.bind("<c>", self.clear)
        self.root.bind("<space>", self.hint_moves)
        self.root.bind("<<MoveConfirmation>>", self.show_moves_if_persistent)
        self.root.bind("<<MoveBack>>", self.show_moves_if_persistent_back)

    def show_moves(self, persistent):
        moves = self.human.possible_actions(self.board.board)
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
        moves = self.human.possible_actions(self.board.board)
        for move in moves:
            start = move.from_square
            self.board.highlight(start)