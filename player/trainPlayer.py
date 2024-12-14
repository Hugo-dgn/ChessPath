import board
import agent

from .openingPlayer import OpeningPlayer

class TrainPlayer(OpeningPlayer):
    
    def __init__(self, board: board.ChessBoard, opening):
        self.trainedColor = opening.color
        self.opening = opening
        self.whiteAgent = agent.OpeningAgent(opening, isHuman=self.trainedColor)
        self.blackAgent = agent.OpeningAgent(opening, isHuman=not self.trainedColor)
        self.openingAgent = agent.OpeningAgent(opening, isHuman=False)
        self.set_trained_color(self.trainedColor)
        OpeningPlayer.__init__(self, board, self.whiteAgent, self.blackAgent, self.openingAgent)

        self.root.bind("<<MoveProcessedBySuperPlayer>>", self.update_success_rate, add=True)
        self.root.bind("<<Reset>>", self.move_on_reset, add=True)
    
    def set_trained_color(self, color):
        pass
    
    def update_success_rate(self, event):
        """flag1, flag2 = self.get_flags()
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
        return flag1, flag2"""
        pass
    
    def move_on_reset(self, event):
        if not self.trainedColor:
            self.forward(event)