import tkinter as tk
import chess
import chess.svg

from .assets import load_chess_pieces as _load_chess_pieces
from .assets import load_chess_pieces_rect as _load_chess_pieces_rect
from .assets import extract_piece as _extract_piece
from .mapping import get_square_pos as _get_square_pos
from .mapping import get_square_from_click as _get_square_from_click

COLOR_WHITE_SQUARE = "#B3B6B7"
COLOR_BLACK_SQUARE = "#A04000"

square_to_radius_ratio = 4
square_to_arrow_width_ratio = 6
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
        self._persistent_arrow_line = []
        self._circle = []
        
        self.arrow_coords = []
        
        self._button3 = None
        
        self.canvas.bind("<ButtonPress-3>", self._clickPress3)
        self.canvas.bind("<ButtonRelease-3>", self._clickRelease3)
        
        self.canvas.bind("<ButtonPress-1>", self._clickPress1)
        self.canvas.bind("<ButtonRelease-1>", self._clickRelease1)
        
        self.canvas.bind("<B1-Motion>", self._motion)
        
        #bind to c press
        self.root.bind("<c>", self._clear)
        
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
        
        self.root.after(1000, lambda: self.root.event_generate("<<Start>>"))
    
    def _draw_piece(self, piece, square, scale):
        piece_image = _extract_piece(self._chess_pieces, self._chess_pieces_rect[piece], int(scale*self.square_size))
        tk_piece_image = self.canvas.create_image(_get_square_pos(square, self.square_size, self.is_flipped), image=piece_image, anchor=tk.NW, tag="piece")
        self._square_images[square] = (tk_piece_image, piece_image)
    
    def order_layer(self):
        self.canvas.tag_raise("piece")
        self.canvas.tag_raise("arrow")
    
    def draw(self):
        position = "".join(reversed(self.board.epd().split()[0].split("/")))
        
        square = 0
        self._square_images = [None]*64
        
        for piece in position:
            if piece.isdigit():
                square += int(piece)
            else:
                self._draw_piece(piece, square, 1)
                square += 1
        
        self.order_layer()
        self.canvas.update_idletasks()
    
    def arrow(self, svgArrow, persistent=False):
        self.arrow_coords.append(svgArrow)
        
        start = svgArrow.head
        end = svgArrow.tail
        
        if start == end:
            x, y = _get_square_pos(start, self.square_size, self.is_flipped, center=True)
            r = self.square_size//2
            x -= r
            y -= r
            line = self.canvas.create_rectangle(x, y, x+2*r, y+2*r, fill=svgArrow.color, stipple="gray50", tags="arrow")
            self.order_layer()
        else:
            start_loc = _get_square_pos(start, self.square_size, self.is_flipped, center=True)
            end_loc = _get_square_pos(end, self.square_size, self.is_flipped, center=True)
            
            dx = abs(end_loc[0] - start_loc[0])//self.square_size
            dy = abs(end_loc[1] - start_loc[1])//self.square_size

            mid = None
            if (dx, dy) == (1, 2):
                mid = (start_loc[0], end_loc[1])
            elif (dx, dy) == (2, 1):
                mid = (end_loc[0], start_loc[1])
            
            if mid is not None:
                direction_dx = (mid[0] - start_loc[0])//self.square_size
                direction_dy = (mid[1] - start_loc[1])//self.square_size
            else:
                direction_dx = (end_loc[0] - start_loc[0])//self.square_size
                direction_dy = (end_loc[1] - start_loc[1])//self.square_size
            
            start_loc = list(start_loc)
            if direction_dx < 0:
                start_loc[0] -= self.square_size/3
            elif direction_dx > 0:
                start_loc[0] += self.square_size/3
            if direction_dy < 0:
                start_loc[1] -= self.square_size/3
            elif direction_dy > 0:
                start_loc[1] += self.square_size/3
                
            points = [start_loc]
            if mid is not None:
                points.append(mid)
            points.append(end_loc)
            
            arrow_width = self.square_size//square_to_arrow_width_ratio
            arrow_shape = (arrow_width, arrow_width, arrow_width)
            line = self.canvas.create_line(*points, arrow=tk.LAST, width=arrow_width, arrowshape=arrow_shape, fill=svgArrow.color, stipple="gray75", tags="arrow")
        
        if not persistent:
            self._arrow_line.append(line)
        else:
            self._persistent_arrow_line.append(line)

    def clear(self, clear_persistent=True):
        if self.locked:
            return
        for line in self._arrow_line:
            self.canvas.delete(line)
        
        if clear_persistent:
            for line in self._persistent_arrow_line:
                self.canvas.delete(line)
        for circle in self._circle:
            self.canvas.delete(circle)
        self._arrow_line = []
        if clear_persistent:
            self._persistent_arrow_line = []
        self._circle = []
        self.arrow_coords = []
        
    def _clear(self, event):
        self.clear()
    
    def _clickRelease1(self, event):
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
    
    def _clickPress1(self, event):
        if self.locked:
            return
        
        flag = self._clickRelease1(event)
        if flag:
            return
        
        self.clear(clear_persistent=False)
        
        square = _get_square_from_click(event.x, event.y, self.square_size, self.is_flipped)
        piece = self.board.piece_at(square)
        if piece is not None:
            self.selected_square = square
            self.hold = True
            
            self._draw_piece(piece.symbol(), square, hold_size_ratio)
            self._motion(event)
            
            legal_moves = self.board.legal_moves
            possible_moves = [move.to_square for move in legal_moves if move.from_square == square]
            for center in possible_moves:
                x, y = _get_square_pos(center, self.square_size, self.is_flipped, center=True)
                r = self.square_size//square_to_radius_ratio
                x -= r
                y -= r
                circle = self.canvas.create_oval(x, y, x+2*r, y+2*r, fill="grey", stipple="gray50")
                self._circle.append(circle)
    
    def _clickPress3(self, event):
        if self.locked:
            return
        
        square = _get_square_from_click(event.x, event.y, self.square_size, self.is_flipped)
        self._button3 = square
    
    def _clickRelease3(self, event):
        if self.locked:
            return
        square = _get_square_from_click(event.x, event.y, self.square_size, self.is_flipped)
        svgArrow = chess.svg.Arrow(square, self._button3, color="orange")
        self.arrow(svgArrow)
    
    def _motion(self, event):
        if self.locked:
            return
        if self.hold:
            image_id, _ = self._square_images[self.selected_square]
            ofset = hold_size_ratio*self.square_size//2
            self.canvas.moveto(image_id, event.x - ofset, event.y - ofset)
    
    def _promotion_panel(self, move):
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
    
    def push(self, move, generateEvent=True):
        flag = False
        if self.board.is_legal(move):
            for circle in self._circle:
                self.canvas.delete(circle)
            self.board.push(move)
            flag = True
        else:
            move.promotion = chess.QUEEN
            if self.board.is_legal(move):
                self._promotion_panel(move)
                self.board.push(move)
                flag = True
        
        self.draw()
        if flag and generateEvent:
            self.root.event_generate("<<MoveConfirmation>>")
        return flag

    def back(self):
        self.board.pop()
        self.draw()
    
    def flip(self):
        self.is_flipped = not self.is_flipped
        self.draw()
    
    def reset(self, fen=None, flipped=None):
        if fen is not None:
            self.board.set_fen(fen)
        else:
            self.board.reset()
        if flipped is not None:
            self.is_flipped = flipped
        self.draw()

def _draw_board(root, case_size):
    canvas = tk.Canvas(root, width=case_size*8,
                        height=case_size*8)
    for i in range(8):
        for j in range(8):
            if (i+j) % 2:
                color = COLOR_BLACK_SQUARE
            else:
                color = COLOR_WHITE_SQUARE
            canvas.create_rectangle(i*case_size, j*case_size,
                                (i+1)*case_size, (j+1)*case_size,
                                fill=color, outline="")
    return canvas