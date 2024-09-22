import agent.humanTrainOpeningAgent
import board
import agent
import database
import database.openings

from .openingPlayer import OpeningPlayer

class TrainPlayer(OpeningPlayer):
    
    def __init__(self, board: board.ChessBoard, openingName : str, color : bool):
        OpeningPlayer.__init__(self, board, openingName, color)
        
        if color:
            self.whiteAgent = agent.HumanTrainOpeningAgent(self.opening)
            self.blackAgent = agent.TrainOpeningAgent(self.opening)
        else:
            self.whiteAgent = agent.TrainOpeningAgent(self.opening)
            self.blackAgent = agent.HumanTrainOpeningAgent(self.opening)
    
        self.root.bind("<<MoveConfirmation>>", self.update_success_rate)
    
    def update_success_rate(self, event):
        last_move = self.board.board.peek()
        self.opening.root()
        for move in self.board.board.move_stack[:-1]:
            self.opening.push(move)
        node = self.opening.cursor
        flag1, flag2 = self.move(event, False)
        if not flag1:
            for link in node.children:
                link.visits += 1
        else:
            for link in node.children:
                if link.move == last_move:
                    link.visits += 1
                    link.successes += 1
        
        