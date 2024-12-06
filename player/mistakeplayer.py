import chess.svg

from board import ChessBoard
import agent
from .trainPlayer import TrainPlayer

class MistakePlayer(TrainPlayer):

    def __init__(self, white_mistake, black_mistake, board: ChessBoard, auto_next):
        self.white_mistake = white_mistake
        self.black_mistake = black_mistake
        
        self.auto_next = auto_next
        self.current_mistake = None
        
        TrainPlayer.__init__(self, board, None, None)
        
        self.buffer_white_agent = self.whiteAgent
        self.buffer_black_agent = self.blackAgent
        
        self.root.bind("<M>", self.next_mistake)
        self.root.bind("<m>", lambda event : self.go_to_mistake())
        
        self.root.bind("<<MoveProcessedBySuperPlayer>>", self.check_auto_next, add=True)
        
        self.mistake_position = None
        
        self.next_mistake(None)
    
    def go_to_mistake(self):
        self.board.reset()
        pgn_agent = agent.pgnAgent.PgnAgent(self.current_mistake['pgn'])
        self.whiteAgent = pgn_agent
        self.blackAgent = pgn_agent
        
        mistake_move = self.current_mistake['move']
        color = self.opening.color
        
        for _ in range(2*mistake_move-color-1):
            move = pgn_agent.act(self.board.board, True)
            self.board.push(move, generateEvent=False)
            
        self.whiteAgent = self.buffer_white_agent
        self.blackAgent = self.buffer_black_agent
        
        wrong_move = pgn_agent.act(self.board.board, True)
        start = wrong_move.from_square
        end = wrong_move.to_square
        
        arrow = chess.svg.Arrow(end, start, color="red")
        self.board.arrow(arrow, persistent=True)

    def next_mistake(self, event):
        self.lock_auto_next = True
        self.current_mistake = self.get_next_mistake()
        
        if self.current_mistake is None:
            return
        
        op = self.current_mistake['opening']
        color = op.color
        
        self.board.clear()
        self.board.reset(flipped=not color)

        self.opening = op
        self.opening.root()
        self.set_trained_color(color)

        self.buffer_white_agent = self.whiteAgent
        self.buffer_black_agent = self.blackAgent
        
        self.go_to_mistake()
    
    def get_next_mistake(self):
        mistake = None
        if len(self.white_mistake) > 0:
            mistake = self.white_mistake.pop()
        elif len(self.black_mistake) > 0:
            mistake = self.black_mistake.pop()
        else:
            print("\nNo more mistakes")
            return None
        print(f"{mistake['pgn'].headers['Link']} ; move {mistake['move']} ; {mistake['opening'].name}")
        return mistake

    def check_auto_next(self, event):
        flag1, flag2 = self.get_flags()
        if flag1 and self.auto_next:
            self.next_mistake(None)
        