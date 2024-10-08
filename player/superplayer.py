import board
import agent

class Player:
    def __init__(self, board : board.ChessBoard, whiteAgent : agent.superAgent, blackAgent : agent.superAgent):
        self.board = board
        self.whiteAgent = whiteAgent
        self.blackAgent = blackAgent
        
        self.root = board.root
        self.root.focus_set()
        self.root.bind("<<MoveConfirmation>>", lambda event : self.move(event, False))
        self.root.bind("<Left>", self.back)
        self.root.bind("<Right>", self.forward)
        self.root.bind("<r>", self.reset)
        
        self.lock = False
    
    def forward(self, event):
        self.root.event_generate("<<ForwardCall>>")
        if len(self.board.board.move_stack) == 0:
            self.start(event, True)
        else:
            self.move(event, True)
    
    def back(self, event):
        if len(self.board.board.move_stack) == 0:
            return
        if self.lock:
            return
        self.board.back()
        self.root.event_generate("<<MoveBack>>")

    def move(self, event, forward):
        if self.lock:
            self.board.back()
            return
        self.lock = True
        _board  = self.board.board.copy()
        last_move = _board.pop()
        flag1 = self.move_confirmation(_board, last_move)
        if not flag1:
            self.board.back()
        
        move = self.agent_action(forward)
        self.lock = False
        flag2 = move is not None
        if flag2:
            self.board.push(move)
        
        return flag1, flag2
    
    def start(self, event, forward):
        move = self.agent_action(forward)
        if move is not None:
            self.board.push(move)
    
    def agent_action(self, forward):
        color = self.board.board.turn
        if color:
            move = self.whiteAgent.act(self.board.board, forward)
        else:
            move = self.blackAgent.act(self.board.board, forward)
        return move
        
    def move_confirmation(self, board, move):
        color = board.turn
        if color:
            flag = self.whiteAgent.is_possible_action(board, move)
        else:
            flag = self.blackAgent.is_possible_action(board, move)
        return flag

    def reset(self, event):
        self.board.reset()
        self.root.event_generate("<<Reset>>")
        self.lock = False