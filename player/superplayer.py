import board
import agent
import webbrowser

class Player:
    def __init__(self, board : board.ChessBoard, whiteAgent : agent.superAgent, blackAgent : agent.superAgent):
        self.board = board
        self.whiteAgent = whiteAgent
        self.blackAgent = blackAgent
        
        self._whiteAgent = whiteAgent
        self._blackAgent = blackAgent
        
        self.is_toggle = False
        
        self.root = board.root
        self.root.focus_set()
        self.root.bind("<<MoveConfirmation>>", lambda event : self.move(event, False))
        self.root.bind("<Left>", self.back)
        self.root.bind("<Right>", self.forward)
        self.root.bind("<r>", self.reset)
        self.root.bind("<a>", self.anchor)
        self.root.bind("<A>", self.go_to_anchor)
        self.root.bind("<t>", self.toggle)
        self.root.bind("<l>", self.open_lichess_analysis)
        
        self.lock = False
        
        self._flag1 = None
        self._flag2 = None
    
    def get_flags(self):
        return self._flag1, self._flag2
    
    def forward(self, event):
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
            return
        
        move = self.agent_action(forward)
        self.lock = False
        flag2 = move is not None
        if flag2:
            self.board.push(move, generateEvent=False)
            
        self._flag1 = flag1
        self._flag2 = flag2
        self.root.event_generate("<<MoveProcessedBySuperPlayer>>")
    
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
    
    def anchor(self, event):
        self.anchor_fen = self.board.board.fen()
        
    def go_to_anchor(self, event):
        if self.anchor_fen is None:
            return
        self.board.reset(self.anchor_fen)
    
    def toggle(self, event):
        if not self.is_toggle:
            self.whiteAgent = agent.Agent()
            self.blackAgent = agent.Agent()
        else:
            self.whiteAgent = self._whiteAgent
            self.blackAgent = self._blackAgent
        self.is_toggle = not self.is_toggle
        
    def open_lichess_analysis(self, event):
        moves = []
        _board = self.board.board.copy()
        while len(_board.move_stack) > 0:
            move = _board.pop()
            san = _board.san(move)
            moves.insert(0, san)
        pgn = "_".join(moves)
        URL =  "https://lichess.org/analysis/pgn/" + pgn
        webbrowser.open(URL)