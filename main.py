import tkinter as tk

import board

root = tk.Tk()
board_frame = tk.Frame(root)
chess_board = board.ChessBoard(board_frame, 64)

def start():
    chess_board.canvas.pack()
    board_frame.pack()
    chess_board.draw()
    root.mainloop()
    
start()