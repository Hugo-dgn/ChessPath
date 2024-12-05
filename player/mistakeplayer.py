from board import ChessBoard
import agent
from .trainPlayer import TrainPlayer

class MistakePlayer(TrainPlayer):

    def __init__(self, white_mistake, black_mistake, board: ChessBoard, auto_next):
        self.white_mistake = white_mistake
        self.black_mistake = black_mistake
        
        self.auto_next = auto_next
        self.current_mistake = None
        
        TrainPlayer.__init__(self, board, "", True, False)
        
        self.buffer_white_agent = self.whiteAgent
        self.buffer_black_agent = self.blackAgent
        
        self.root.bind("<M>", self.next_mistake)
        self.root.bind("<m>", lambda event : self.go_to_mistake())
        
        self.root.bind("<<MoveConfirmation>>", self.check_auto_next)
        
        self.next_mistake(None)
    
    def go_to_mistake(self):
        self.board.reset()
        pgn_agent = agent.pgnAgent.PgnAgent(self.current_mistake['pgn'])
        self.whiteAgent = pgn_agent
        self.blackAgent = pgn_agent
        for i in range(2*self.current_mistake['move']-1*self.current_mistake['color']-1):
            move = pgn_agent.act(self.board.board, True)
            self.board.push(move)
            
        self.whiteAgent = self.buffer_white_agent
        self.blackAgent = self.buffer_black_agent
        
        wrong_move = pgn_agent.act(self.board.board, True)
        start = wrong_move.from_square
        end = wrong_move.to_square
        self.board.arrow(start, end, persistent=True, fill="red")
    
    def next_mistake(self, event):
        self.current_mistake = self.get_next_mistake()
        opName = self.current_mistake['name']
        opColor = self.current_mistake['color']
        
        self.board.reset(flipped=not opColor)

        self.load(opName, opColor)
        
        self.set_trained_color(opColor)
        self.buffer_white_agent = self.whiteAgent
        self.buffer_black_agent = self.blackAgent
        
        self.go_to_mistake()
    
    def get_next_mistake(self):
        mistake = None
        if len(self.white_mistake) > 0:
            mistake = self.white_mistake.pop()
        elif len(self.black_mistake) > 0:
            mistake = self.black_mistake.pop()
        print(f"{mistake['pgn'].headers['Link']} ; move {mistake['move']} ; {mistake['name']}")
        return mistake

    def check_auto_next(self, event):
        flag1, flag2 = self.update_success_rate(None)
        if flag2 and self.auto_next:
            self.next_mistake(None)
        