import tkinter as tk
import argparse

import board
import database
import database.openings

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

def db_command(args):
    if args.name == "op":
        if args.command == "reset":
            database.openings.reset()
        elif args.command == "tables":
            tables = database.openings.tables()
            print(tables)
        elif args.command == "names":
            names = database.openings.openings()
            print(names)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chess game")
    
    subparsers = parser.add_subparsers(dest="command")
    
    board_parser = subparsers.add_parser("board", help="Chess board")
    board_parser.add_argument("--size", type=int, default=64, help="Size of a square")
    board_parser.add_argument("--fliped", action="store_true", help="Is the board fliped")
    board_parser.set_defaults(func=board_window)
    
    db_parser = subparsers.add_parser("db", help="Database")
    db_subparsers = db_parser.add_subparsers(dest="name")
    db_op_subparsers = db_subparsers.add_parser("op", help="Openings")
    db_op_subparsers.add_argument("command", choices = ["reset", "tables", "names"])
    db_parser.set_defaults(func=db_command)
    
    
    args = parser.parse_args()
    args.func(args)