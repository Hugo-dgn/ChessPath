import chess.svg
import chess

import utils

from board import ChessBoard
import agent
from .openingPlayer import OpeningPlayer

class MistakePlayer(OpeningPlayer):

    def __init__(self, mistakes, board: ChessBoard, auto_next, auto_next_eol):
        
        mistakes = [(key, mistakes[key]) for key in mistakes]
        self.mistakes = sorted(mistakes, key=lambda x: x[1]["n"])
        
        self.number_of_mistakes = len(self.mistakes)
        
        self.auto_next = auto_next
        self.auto_next_eol = auto_next_eol
        self.current_mistake_fen = None
        self.current_mistake_moves_data = None
        self.mistake_color = None
        
        white, black = utils.get_openings()
        
        self.whiteAgentHuman = agent.MultiOpeningAgent(white, isHuman=True)
        self.whiteAgentTrain = agent.MultiOpeningAgent(white, isHuman=False)
        
        self.blackAgentHuman = agent.MultiOpeningAgent(black, isHuman=True)
        self.blackAgentTrain = agent.MultiOpeningAgent(black, isHuman=False)
        
        OpeningPlayer.__init__(self, board, None, None, None)
        
        self.root.bind("<M>", self.next_mistake)
        self.root.bind("<m>", lambda event : self.go_to_mistake())
        
        self.root.bind("<<MoveProcessedBySuperPlayer>>", self.check_auto_next, add=True)
        
        self.mistake_position = None
        
        self.next_mistake(None)
    
    def go_to_mistake(self):
        self.board.clear()
        self.board.reset(flipped=not self.mistake_color)
        
        stack = self.current_mistake_moves_data["staks"][0]
        self.whiteAgent.lock = False
        self.blackAgent.lock = False
        for move in stack:
            self.board.push(move)
        self.whiteAgent.lock = True
        self.blackAgent.lock = True
        
        for wrong_move in self.current_mistake_moves_data["moves"]:
            start = wrong_move.from_square
            end = wrong_move.to_square
            
            arrow = chess.svg.Arrow(end, start, color="red")
            self.board.arrow(arrow, persistent=True)

    def next_mistake(self, event):
        self.lock_auto_next = True
        mistake = self.get_next_mistake()
        fen = mistake[0]
        data = mistake[1]
        self.current_mistake_fen = fen
        self.current_mistake_moves_data = data
        
        if self.current_mistake_fen is None:
            return
        
        board = chess.Board(fen=self.current_mistake_fen)
        self.mistake_color = board.turn
        
        if self.mistake_color:
            self.whiteAgent = self.whiteAgentHuman
            self.blackAgent = self.whiteAgentTrain
            self.openingAgent = self.whiteAgentTrain
        else:
            self.whiteAgent = self.blackAgentTrain
            self.blackAgent = self.blackAgentHuman
            self.openingAgent = self.blackAgentTrain
        
        
        ops = self.openingAgent.get_valid_openings(board)
        names = [op.name for op in ops]
        names = ", ".join(names)
        print(f"({self.number_of_mistakes - len(self.mistakes)}/{self.number_of_mistakes}) : {data['n']} mistakes in {names}")
        
        self.go_to_mistake()
    
    def get_next_mistake(self):
        if len(self.mistakes) == 0:
            return None
        else:
            return self.mistakes.pop()

    def check_auto_next(self, event):
        flag1, flag2 = self.get_flags()
        if flag1:
            if self.auto_next:
                self.next_mistake(None)
            if self.auto_next_eol:
                if self.mistake_color:
                    next_moves = self.blackAgent.possible_actions(self.board.board)
                else:
                    next_moves = self.whiteAgent.possible_actions(self.board.board)
                if len(next_moves) == 0:
                    self.next_mistake(None)
        