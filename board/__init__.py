import tkinter as tk
import chess

from .assets import load_chess_pieces as _load_chess_pieces
from .assets import load_chess_pieces_rect as _load_chess_pieces_rect
from .assets import extract_piece as _extract_piece
from .maping import get_square_pos as _get_square_pos
from .maping import get_square_from_click as _get_square_from_click

square_to_radius_ratio = 4
square_to_arrow_width_ratio = 5
hold_size_ratio = 1.5

class ChessBoard:
    
    def __init__(self, root, square_size):
        self.board = chess.Board()
        
        self.square_size = square_size
        
        self.root = root
        self.canvas = _draw_board(root, square_size)
        
        self.is_flipped = False
        self.locked = False
        
        self.selected_square = None
        self.hold = False
        
        self._chess_pieces = _load_chess_pieces()
        self._chess_pieces_rect = _load_chess_pieces_rect()
        self._square_images = [None]*64
        self._arrow_line = []
        self._circle = []
        
        self._button3 = None
        
        self.canvas.bind("<ButtonPress-3>", self.clickPress3)
        self.canvas.bind("<ButtonRelease-3>", self.clickRelease3)
        
        self.canvas.bind("<ButtonPress-1>", self.clickPress1)
        self.canvas.bind("<ButtonRelease-1>", self.clickRelease1)
        
        self.canvas.bind("<B1-Motion>", self.motion)
        
        self._promotion_frame = tk.Frame(root)
        self._Promotion_frame = tk.Frame(root)
        
        self._queen_image = _extract_piece(self._chess_pieces, self._chess_pieces_rect['q'], square_size)
        self._rook_image = _extract_piece(self._chess_pieces, self._chess_pieces_rect['r'], square_size)
        self._bishop_image = _extract_piece(self._chess_pieces, self._chess_pieces_rect['b'], square_size)
        self._knight_image = _extract_piece(self._chess_pieces, self._chess_pieces_rect['n'], square_size)
        
        self._Queen_image = _extract_piece(self._chess_pieces, self._chess_pieces_rect['Q'], square_size)
        self._Rook_image = _extract_piece(self._chess_pieces, self._chess_pieces_rect['R'], square_size)
        self._Bishop_image = _extract_piece(self._chess_pieces, self._chess_pieces_rect['B'], square_size)
        self._Knight_image = _extract_piece(self._chess_pieces, self._chess_pieces_rect['N'], square_size)
        
        
        self._queen_button = tk.Button(self._promotion_frame, image=self._queen_image, command=self._queen_promotion)
        self._rook_button = tk.Button(self._promotion_frame, image=self._rook_image, command=self._rook_promotion)
        self._bishop_button = tk.Button(self._promotion_frame, image=self._bishop_image, command=self._bishop_promotion)
        self._knight_button = tk.Button(self._promotion_frame, image=self._knight_image, command=self._knight_promotion)
        self._back_button = tk.Button(self._promotion_frame, text="Back", command=self._back_promotion)
        
        self._Queen_button = tk.Button(self._Promotion_frame, image=self._Queen_image, command=self._queen_promotion)
        self._Rook_button = tk.Button(self._Promotion_frame, image=self._Rook_image, command=self._rook_promotion)
        self._Bishop_button = tk.Button(self._Promotion_frame, image=self._Bishop_image, command=self._bishop_promotion)
        self._Knight_button = tk.Button(self._Promotion_frame, image=self._Knight_image, command=self._knight_promotion)
        self._Back_button = tk.Button(self._Promotion_frame, text="Back", command=self._back_promotion)
        
        self._queen_button.grid(row=0, column=0)
        self._rook_button.grid(row=1, column=0)
        self._bishop_button.grid(row=2, column=0)
        self._knight_button.grid(row=3, column=0)
        self._back_button.grid(row=4, column=0)
        
        self._Queen_button.grid(row=0, column=0)
        self._Rook_button.grid(row=1, column=0)
        self._Bishop_button.grid(row=2, column=0)
        self._Knight_button.grid(row=3, column=0)
        self._Back_button.grid(row=4, column=0)
        
        self._button_window = None
        self._promotion_move = None
    
    def draw_piece(self, piece, square, scale):
        piece_image = _extract_piece(self._chess_pieces, self._chess_pieces_rect[piece], int(scale*self.square_size))
        tk_piece_image = self.canvas.create_image(_get_square_pos(square, self.square_size, self.is_flipped), image=piece_image, anchor=tk.NW)
        self._square_images[square] = (tk_piece_image, piece_image)
    
    def draw(self):
        position = "".join(reversed(self.board.epd().split()[0].split("/")))
        
        square = 0
        self._square_images = [None]*64
        
        for piece in position:
            if piece.isdigit():
                square += int(piece)
            else:
                self.draw_piece(piece, square, 1)
                square += 1
    
    def arrow(self, start, end):
        start_loc = _get_square_pos(start, self.square_size, self.is_flipped, center=True)
        end_loc = _get_square_pos(end, self.square_size, self.is_flipped, center=True)
        dx = abs(end_loc[0] - start_loc[0])//self.square_size
        dy = abs(end_loc[1] - start_loc[1])//self.square_size

        points = [start_loc]
        if (dx, dy) == (1, 2):
            mid = (start_loc[0], end_loc[1])
            points.append(mid)
        elif (dx, dy) == (2, 1):
            mid = (end_loc[0], start_loc[1])
            points.append(mid)
        points.append(end_loc)
        
        line = self.canvas.create_line(*points, arrow=tk.LAST, width=self.square_size//square_to_arrow_width_ratio, fill="orange", stipple="gray50")
        self._arrow_line.append(line)
    
    def clickRelease1(self, event):
        if self.locked:
            return
        
        legal = False
        if self.selected_square is not None:
            square = _get_square_from_click(event.x, event.y, self.square_size, self.is_flipped)
            move = chess.Move(self.selected_square, square)
            legal = self.push(move)
            if not self.hold:
                self.selected_square = None
            self.hold = False
        return legal
    
    def clickPress1(self, event):
        if self.locked:
            return
        
        flag = self.clickRelease1(event)
        if flag:
            return
        
        for line in self._arrow_line:
            self.canvas.delete(line)
        for circle in self._circle:
            self.canvas.delete(circle)
        self._arrow_line = []
        self._circle = []
        
        square = _get_square_from_click(event.x, event.y, self.square_size, self.is_flipped)
        piece = self.board.piece_at(square)
        if piece is not None:
            self.selected_square = square
            self.hold = True
            
            self.draw_piece(piece.symbol(), square, hold_size_ratio)
            self.motion(event)
            
            legal_moves = self.board.legal_moves
            possible_moves = [move.to_square for move in legal_moves if move.from_square == square]
            for center in possible_moves:
                x, y = _get_square_pos(center, self.square_size, self.is_flipped, center=True)
                r = self.square_size//square_to_radius_ratio
                x -= r
                y -= r
                circle = self.canvas.create_oval(x, y, x+2*r, y+2*r, fill="grey", stipple="gray50")
                self._circle.append(circle)
    
    def clickPress3(self, event):
        if self.locked:
            return
        
        square = _get_square_from_click(event.x, event.y, self.square_size, self.is_flipped)
        self._button3 = square
    
    def clickRelease3(self, event):
        if self.locked:
            return
        square = _get_square_from_click(event.x, event.y, self.square_size, self.is_flipped)
        self.arrow(self._button3, square)
    
    def motion(self, event):
        if self.locked:
            return
        if self.hold:
            image_id, _ = self._square_images[self.selected_square]
            ofset = hold_size_ratio*self.square_size//2
            self.canvas.moveto(image_id, event.x - ofset, event.y - ofset)
            self.canvas.update()
    
    def promotion_panel(self, move):
        if self.board.turn:
            panel = self._Promotion_frame
        else:
            panel = self._promotion_frame
        
        square = move.to_square
        x, y = _get_square_pos(square, self.square_size, self.is_flipped)
        if y == 0:
            anchor = "nw"
        else:
            anchor = "sw"
            y += self.square_size
        self._button_window = self.canvas.create_window(x, y, window=panel, anchor=anchor)
        self.locked = True
        self._promotion_move = move
    
    def _promotion(self):
        self.locked = False
        self.canvas.delete(self._button_window)
        self.board.pop()
        if self._promotion_move.promotion is not None:
            self.push(self._promotion_move)
        else:
            self.draw()
        
    
    def _queen_promotion(self):
        self._promotion_move.promotion = chess.QUEEN
        self._promotion()
    
    def _rook_promotion(self):
        self._promotion_move.promotion = chess.ROOK
        self._promotion()
    
    def _bishop_promotion(self):
        self._promotion_move.promotion = chess.BISHOP
        self._promotion()
    
    def _knight_promotion(self):
        self._promotion_move.promotion = chess.KNIGHT
        self._promotion()
    
    def _back_promotion(self):
        self._promotion_move.promotion = None
        self._promotion()
    
    def push(self, move):
        flag = False
        if self.board.is_legal(move):
            for circle in self._circle:
                self.canvas.delete(circle)
            self.board.push(move)
            self.root.event_generate("<<MoveConfirmation>>")
            flag = True
        else:
            move.promotion = chess.QUEEN
            if self.board.is_legal(move):
                self.promotion_panel(move)
                self.board.push(move)
        self.draw()
        return flag

    def back(self):
        self.board.pop()
        self.draw()
    
    def reset(self):
        self.board.reset()
        self.draw()

def _draw_board(root, case_size):
    canvas = tk.Canvas(root, width=case_size*8,
                        height=case_size*8)
    for i in range(8):
        for j in range(8):
            if (i+j) % 2:
                color = "#A04000"
            else:
                color = "#B3B6B7"
            canvas.create_rectangle(i*case_size, j*case_size,
                                (i+1)*case_size, (j+1)*case_size,
                                fill=color, outline="")
    return canvas