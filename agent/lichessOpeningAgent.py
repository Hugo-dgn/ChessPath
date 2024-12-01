import chess
import random

from .superAgent import Agent

import lichess

class LichessOpeningAgent(Agent):
    
    def __init__(self, rating_range, time_control, number_of_moves):
        Agent.__init__(self)
        self.rating_range = rating_range
        self.time_control = time_control
        self.number_of_moves = number_of_moves
        
        self.memory = {}
    
    def get_moves_info(self, fen):
        if fen in self.memory:
            moves_info = self.memory[fen]
        else:
            moves_info = lichess.get_most_common_moves(fen, self.rating_range, self.time_control, self.number_of_moves)
            self.memory[fen] = moves_info
        return moves_info
    
    def is_possible_action(self, board, move):
        moves = self.possible_actions(board)
        return move in moves
    
    def act(self, board, forwardCall):
        moves_info = self.get_moves_info(board.fen())
        if len(moves_info) == 0:
            return None
        moves = [chess.Move.from_uci(move_info["uci"]) for move_info in moves_info]
        occurences = [move_info["white"] + move_info["black"] + move_info["draws"] for move_info in moves_info]
        probabilities = [occurence/sum(occurences) for occurence in occurences]
        move = random.choices(moves, probabilities)[0]
        return move
    
    def possible_actions(self, board):
        moves_info = self.get_moves_info(board.fen())
        moves = [chess.Move.from_uci(move_info["uci"]) for move_info in moves_info]
        return moves