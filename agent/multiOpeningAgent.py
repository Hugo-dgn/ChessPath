import random

from .openingAgent import OpeningAgent
from .superAgent import Agent

class MultiOpeningAgent(Agent):
    
    def __init__(self, openings, isHuman):
        Agent.__init__(self, isHuman)
        self.agents = []
        for opening in openings:
            self.agents.append(OpeningAgent(opening, isHuman))
    
    def get_valid_openings(self, board):
        valid_openings = []
        for agent in self.agents:
            if len(agent.possible_actions(board)) > 0:
                valid_openings.append(agent.opening)
        return valid_openings
    
    def set_score_function(self, score_function):
        for agent in self.agents:
            agent.set_score_function(score_function)
    
    def act(self, board, forwardCall):
        moves = []
        for agent in self.agents:
            move = agent.act(board, forwardCall)
            if move is not None:
                moves.append(move)
                
        if len(moves) == 0:
            return None
        else:
            return random.choice(moves)
    
    def possible_actions(self, board):
        moves = []
        for agent in self.agents:
            moves += agent.possible_actions(board)
        return moves

    def is_possible_action(self, board, move):
        for agent in self.agents:
            if agent.is_possible_action(board, move):
                return True
        return False
    
    def get_arrow_annotations(self, board):
        annotations = []
        for agent in self.agents:
            annotations += agent.get_arrow_annotations(board)
        return annotations

    