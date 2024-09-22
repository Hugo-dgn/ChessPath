import board
import agent
import database
import database.openings

from .superplayer import Player

class Openingplayer(Player):
    
    def __init__(self, board: board.ChessBoard, openingName : str, color : bool):
        op = database.openings.load(openingName, color)
        
        if color:
            whiteAgent = agent.HumanOpeningAgent(op)
            blackAgent = agent.OpeningAgent(op)
            self.human = whiteAgent
        else:
            whiteAgent = agent.OpeningAgent(op)
            blackAgent = agent.HumanOpeningAgent(op)
            self.human = blackAgent
        
        Player.__init__(self, board, whiteAgent, blackAgent)
        
        self.root.bind("<s>", self.show_moves)
        #bind space bar
        self.root.bind("<space>", self.hint_moves)
    
    def show_moves(self, event):
        moves = self.human.possible_actions(self.board.board)
        for move in moves:
            start = move.from_square
            end = move.to_square
            self.board.arrow(start, end)
    
    def hint_moves(self, event):
        moves = self.human.possible_actions(self.board.board)
        for move in moves:
            start = move.from_square
            self.board.highlight(start)