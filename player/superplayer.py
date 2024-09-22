import board
import agent

class Player:
    def __init__(self, board : board.ChessBoard, whiteAgent : agent.superAgent, blackAgent : agent.superAgent):
        self.board = board
        self.whiteAgent = whiteAgent
        self.blackAgent = blackAgent
        
        self.root = board.root
        self.root.focus_set()
        self.root.bind("<<MoveConfirmation>>", self.move)
        self.root.bind("<<Start>>", self.start)
        self.root.bind("<Left>", self.back)
        self.root.bind("<Right>", self.forward)
        
        self.lock = False
    
    def forward(self, event):
        self.root.event_generate("<<MoveConfirmation>>")
    
    def back(self, event):
        if len(self.board.board.move_stack) == 0:
            return
        if self.lock:
            return
        self.board.back()

    def move(self, event):
        if self.lock:
            self.board.back()
            return
        self.lock = True
        _board  = self.board.board.copy()
        last_move = _board.pop()
        flag = self.move_confirmation(_board, last_move)
        if not flag:
            self.board.back()
        
        move = self.agent_action()
        
        self.lock = False
        if move is not None:
            self.board.push(move)
    
    def start(self, event):
        move = self.agent_action()
        if move is not None:
            self.board.push(move)
    
    def agent_action(self):
        color = self.board.board.turn
        if color:
            move = self.whiteAgent.act(self.board.board)
        else:
            move = self.blackAgent.act(self.board.board)
        return move
        
    def move_confirmation(self, board, move):
        color = board.turn
        if color:
            flag = self.whiteAgent.is_possible_action(board, move)
        else:
            flag = self.blackAgent.is_possible_action(board, move)
        return flag