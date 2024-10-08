import tkinter as tk
import argparse
import chess

import board
import player
import agent
import database
import opening

def get_board(args):
    args.color = args.color == "w"
    root = tk.Tk()
    board_frame = tk.Frame(root)
    chess_board = board.ChessBoard(board_frame, args.size)
    if args.fliped:
        chess_board.flip()
    chess_board.canvas.pack()
    board_frame.pack()
    chess_board.draw()
    return chess_board, root

def board_window(args):
    chess_board, root = get_board(args)
    root.mainloop()

def player_window(args):
    chess_board, root = get_board(args)
    
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

def openingPlayer_window(args):
    chess_board, root = get_board(args)
    op_player = player.OpeningPlayer(chess_board, args.opening, args.color)
    root.mainloop()

def editor_window(args):
    chess_board, root = get_board(args)
    editor = player.Editor(chess_board, args.opening, args.color)
    root.mainloop()

def train_window(args):
    chess_board, root = get_board(args)
    train_player = player.TrainPlayer(chess_board, args.opening, args.color)
    root.mainloop()

def db_command(args):
    if hasattr(args, "color"):
        args.color = args.color == "w"
    if args.tables == "op":
        if args.command == "reset":
            database.openings.reset()
        elif args.command == "table":
            df = database.openings.table("openings")
            df = df.drop(columns=['tree'])
            df['color'] = df['color'].replace({1: 'white', 0: 'black'})
            print(df.head())
        elif args.command == "commit":
            if args.action == "create":
                op = opening.Opening(args.name, args.color, opening.Node())
                database.openings.save(op)
            elif args.action == "delete":
                database.openings.delete(args.name, args.color)

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
    
    openingPlayer_parser = subparsers.add_parser("openingPlayer", help="Chess player with opening")
    openingPlayer_parser.add_argument("opening", type=str, help="name of the opening")
    openingPlayer_parser.add_argument("color", type=str, choices=["w", "b"], help="color of the player")
    openingPlayer_parser.add_argument("--size", type=int, default=64, help="Size of a square")
    openingPlayer_parser.add_argument("--fliped", action="store_true", help="Is the board fliped")
    openingPlayer_parser.set_defaults(func=openingPlayer_window)
    
    editor_parser = subparsers.add_parser("editor", help="Opening editor")
    editor_parser.add_argument("opening", type=str, help="name of the opening")
    editor_parser.add_argument("color", type=str, choices=["w", "b"], help="color of the player")
    editor_parser.add_argument("--size", type=int, default=64, help="Size of a square")
    editor_parser.add_argument("--fliped", action="store_true", help="Is the board fliped")
    editor_parser.set_defaults(func=editor_window)
    
    train_parser = subparsers.add_parser("train", help="Train an opening")
    train_parser.add_argument("opening", type=str, help="name of the opening")
    train_parser.add_argument("color", type=str, choices=["w", "b"], help="color of the player")
    train_parser.add_argument("--size", type=int, default=64, help="Size of a square")
    train_parser.add_argument("--fliped", action="store_true", help="Is the board fliped")
    train_parser.set_defaults(func=train_window)
    
    
    db_parser = subparsers.add_parser("db", help="Database")
    db_subparsers = db_parser.add_subparsers(dest="tables")
    db_op_subparsers = db_subparsers.add_parser("op", help="Openings")
    
    db_command_subparsers = db_op_subparsers.add_subparsers(dest="command")
    db_command_subparsers.add_parser("reset", help="Reset the database")
    db_command_subparsers.add_parser("table", help="List tables")
    
    commit_parser = db_command_subparsers.add_parser("commit", help="Change the database")
    commit_parser.add_argument("action", type=str, choices=["create", "delete"], help="Action to perform")
    commit_parser.add_argument("name", type=str, help="Name of the opening")
    commit_parser.add_argument("color", type=str, choices=["w", "b"], help="Color of the opening")
    db_parser.set_defaults(func=db_command)
    
    
    args = parser.parse_args()
    args.func(args)