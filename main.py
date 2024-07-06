import tkinter as tk
import argparse

import board

def board_window(args):
    root = tk.Tk()
    board_frame = tk.Frame(root)
    chess_board = board.ChessBoard(board_frame, args.size)
    if args.fliped:
        chess_board.flip()
    chess_board.canvas.pack()
    board_frame.pack()
    chess_board.draw()
    root.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chess game")
    
    subparsers = parser.add_subparsers(dest="command")
    
    board_parser = subparsers.add_parser("board", help="Chess board")
    board_parser.add_argument("--size", type=int, default=64, help="Size of a square")
    board_parser.add_argument("--fliped", action="store_true", help="Is the board fliped")
    board_parser.set_defaults(func=board_window)
    
    args = parser.parse_args()
    args.func(args)