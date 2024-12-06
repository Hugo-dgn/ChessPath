import agent.humanTrainOpeningAgent
import board
import agent

from .openingPlayer import OpeningPlayer

class TrainPlayer(OpeningPlayer):
    
    def __init__(self, board: board.ChessBoard, opening, trainedColor):
        OpeningPlayer.__init__(self, board, opening)
        self.edit_mode = False
        self.anchor_fen = None

        self.root.bind("<<MoveProcessedBySuperPlayer>>", self.update_success_rate, add=True)
        self.root.bind("<<Reset>>", self.move_on_reset)
        
        self.trainedColor = trainedColor
        self.set_trained_color(trainedColor)
    
    def set_trained_color(self, color):
        self.color = color
        if color:
            self.whiteAgent = agent.HumanTrainOpeningAgent(self.opening)
            self.blackAgent = agent.TrainOpeningAgent(self.opening)
        else:
            self.whiteAgent = agent.TrainOpeningAgent(self.opening)
            self.blackAgent = agent.HumanTrainOpeningAgent(self.opening)
    
    def update_success_rate(self, event):
        flag1, flag2 = self.get_flags()
        if len(self.board.board.move_stack) == 0:
            return flag1, flag2
        last_move = self.board.board.peek()
        self.opening.root()
        for move in self.board.board.move_stack[:-1]:
            self.opening.push(move)
        node = self.opening.cursor
        if not flag1:
            for link in node.children:
                link.visits += 1
        else:
            for link in node.children:
                if link.move == last_move:
                    link.visits += 1
                    link.successes += 1
        return flag1, flag2
    
    def move_on_reset(self, event):
        if not self.color:
            self.forward(event)