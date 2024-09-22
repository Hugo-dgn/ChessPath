import tkinter as tk
import argparse
import chess

import board
import player
import agent
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

def player_window(args):
    root = tk.Tk()
    board_frame = tk.Frame(root)
    chess_board = board.ChessBoard(board_frame, args.size)
    if args.fliped:
        chess_board.flip()
    chess_board.canvas.pack()
    board_frame.pack()
    chess_board.draw()
    
    if args.whiteAgent == "human":
        if args.opening is None:
            op = None
        else:
            op = database.openings.load(args.opening, chess.WHITE)
            if op is None:
                assert False, "Opening not found for white agent"
        if op is None:
            white_agent = agent.Agent()
        else:
            white_agent = agent.HumanOpeningAgent(op)
    else:
        op = database.openings.load(args.whiteAgent, chess.WHITE)
        if op is None:
            assert False, "Opening not found for white agent"
        white_agent = agent.OpeningAgent(op)
            
    if args.blackAgent == "human":
        if args.opening is None:
            op = None
        else:
            op = database.openings.load(args.opening, chess.BLACK)
            if op is None:
                assert False, "Opening not found for black agent"
        if op is None:
            black_agent = agent.Agent()
        else:
            black_agent = agent.HumanOpeningAgent(op)
    else:
        op = database.openings.load(args.blackAgent, chess.BLACK)
        if op is None:
            assert False, "Opening not found for black agent"
        black_agent = agent.OpeningAgent(op)
    base_player = player.Player(chess_board, white_agent, black_agent)
    root.mainloop()

def db_command(args):
    if args.name == "op":
        if args.command == "reset":
            database.openings.reset()
        elif args.command == "table":
            df = database.openings.table("openings")
            df = df.drop(columns=['tree'])
            df['color'] = df['color'].replace({1: 'white', 0: 'black'})
            print(df.head())
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
    
    player_parser = subparsers.add_parser("player", help="Chess player")
    player_parser.add_argument("whiteAgent", type=str, help="name of the white agent")
    player_parser.add_argument("blackAgent", type=str, help="name of the black agent")
    player_parser.add_argument("--opening", type=str, help="name of the opening")
    player_parser.add_argument("--size", type=int, default=64, help="Size of a square")
    player_parser.add_argument("--fliped", action="store_true", help="Is the board fliped")
    player_parser.set_defaults(func=player_window)
    
    db_parser = subparsers.add_parser("db", help="Database")
    db_subparsers = db_parser.add_subparsers(dest="name")
    db_op_subparsers = db_subparsers.add_parser("op", help="Openings")
    db_op_subparsers.add_argument("command", choices = ["reset", "table", "names"])
    db_parser.set_defaults(func=db_command)
    
    
    args = parser.parse_args()
    args.func(args)