import tkinter as tk
import argparse

import board
import player
import agent
import database
import opening
import chesscom
import crawler

#### default values

size = 64

#### functions

def get_board(args):
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
    white_agent = agent.Agent()
    black_agent = agent.Agent()
    base_player = player.Player(chess_board, white_agent, black_agent)
    root.mainloop()

def player_window(args):
    setattr(args, "fliped", args.color == "b")
    color = args.color == "w"
    chess_board, root = get_board(args)
    op = database.openings.load(args.opening, color)
    openingAgent = agent.HumanOpeningAgent(op)
    op_player = player.OpeningPlayer(chess_board, openingAgent, openingAgent, op)
    root.mainloop()

def editor_window(args):
    setattr(args, "fliped", args.color == "b")
    color = args.color == "w"
    chess_board, root = get_board(args)
    op = database.openings.load(args.opening, color)
    editor = player.Editor(chess_board, op)
    root.mainloop()

def train_window(args):
    setattr(args, "fliped", args.color == "b")
    color = args.color == "w"
    chess_board, root = get_board(args)
    op = database.openings.load(args.opening, color)
    train_player = player.TrainPlayer(chess_board, op, color)
    root.mainloop()
    
def mistakes_window(args):
    setattr(args, "fliped", False)
    chess_board, root = get_board(args)
    pgns = chesscom.fetch_chesscom_games(args.user_name, args.date, args.time)
    white_mistakes, black_mistakes = crawler.fromPGN(pgns, 'hugo_dgn', 0)
    print(f"Mistakes found for white : {len(white_mistakes)}")
    print(f"Mistakes found for black : {len(black_mistakes)}")
    print("")
    base_player = player.MistakePlayer(white_mistakes, black_mistakes, chess_board, args.auto_next)
    root.mainloop()

def lichess_sim_window(args):
    setattr(args, "fliped", args.color == "b")
    color = args.color == "w"
    if color:
        white_agent = agent.Agent()
        black_agent = agent.LichessOpeningAgent(args.rating_range, args.time_control, args.number_of_moves)
    else:
        white_agent = agent.LichessOpeningAgent(args.rating_range, args.time_control, args.number_of_moves)
        black_agent = agent.Agent()
    chess_board, root = get_board(args)
    base_player = player.Player(chess_board, white_agent, black_agent)
    root.mainloop()

def db_command(args):
    if hasattr(args, "color"):
        color = args.color == "w"
    else:
        color = None
    if args.tables == "op":
        if args.command == "reset":
            database.openings.reset()
        elif args.command == "table":
            df = database.openings.table("openings")
            df = df.drop(columns=['pgn'])
            df['color'] = df['color'].replace({1: 'white', 0: 'black'})
            print(df.head())
        elif args.command == "pgn":
            if args.pgn_command == "get":
                pgn = database.openings.get_pgn(args.opening, color)
                print(pgn)
            elif args.pgn_command == "set":
                database.openings.set_pgn(args.opening, color, args.pgn)
        elif args.command == "commit":
            if args.action == "create":
                op = opening.Opening(args.name, color, opening.Node())
                database.openings.save(op)
            elif args.action == "delete":
                database.openings.delete(args.name, color)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chess game")
    
    subparsers = parser.add_subparsers(dest="command")
    
    board_parser = subparsers.add_parser("board", help="Chess board")
    board_parser.add_argument("--size", type=int, default=size, help="Size of a square")
    board_parser.add_argument("--fliped", action="store_true", help="Is the board fliped")
    board_parser.set_defaults(func=board_window)
    
    player_parser = subparsers.add_parser("player", help="Chess player")
    player_parser.add_argument("opening", type=str, help="name of the opening")
    player_parser.add_argument("color", type=str, choices=["w", "b"], help="color of the player")
    player_parser.add_argument("--size", type=int, default=size, help="Size of a square")
    player_parser.set_defaults(func=player_window)
    
    editor_parser = subparsers.add_parser("edit", help="Opening editor")
    editor_parser.add_argument("opening", type=str, help="name of the opening")
    editor_parser.add_argument("color", type=str, choices=["w", "b"], help="color of the player")
    editor_parser.add_argument("--size", type=int, default=size, help="Size of a square")
    editor_parser.set_defaults(func=editor_window)
    
    lichess_sim_parser = subparsers.add_parser("lichess-sim", help="Simulate a lichess game")
    lichess_sim_parser.add_argument("color", type=str, choices=["w", "b"], help="Color of the player")
    lichess_sim_parser.add_argument("rating_range", type=int, nargs=2, help="Rating range")
    lichess_sim_parser.add_argument("time_control", type=str, choices=["bullet", "blitz", "rapid", "classical"], help="Time control")
    lichess_sim_parser.add_argument("number_of_moves", type=int, help="Number of moves")
    lichess_sim_parser.add_argument("--size", type=int, default=size, help="Size of a square")
    lichess_sim_parser.set_defaults(func=lichess_sim_window)
    
    train_parser = subparsers.add_parser("train", help="Train an opening")
    train_parser.add_argument("opening", type=str, help="name of the opening")
    train_parser.add_argument("color", type=str, choices=["w", "b"], help="color of the player")
    train_parser.add_argument("--size", type=int, default=size, help="Size of a square")
    train_parser.set_defaults(func=train_window)
    
    mistakes_parser = subparsers.add_parser("mistakes", help="Find mistakes in a PGN")
    mistakes_parser.add_argument("user_name", type=str, help="Chess.com user name")
    mistakes_parser.add_argument("date", type=str, help="Date")
    mistakes_parser.add_argument("time", type=str, help="Time control")
    mistakes_parser.add_argument("--auto-next", action="store_true", help="Auto next mistake")
    mistakes_parser.add_argument("--size", type=int, default=size, help="Size of a square")
    mistakes_parser.set_defaults(func=mistakes_window)
    
    
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
    
    pgn_parser = db_command_subparsers.add_parser("pgn", help="PGN")
    pgn_command_subparsers = pgn_parser.add_subparsers(dest="pgn_command")
    
    pgn_get_parser = pgn_command_subparsers.add_parser("get", help="Get PGN")
    pgn_get_parser.add_argument("opening", type=str, help="Name of the opening")
    pgn_get_parser.add_argument("color", type=str, choices=["w", "b"], help="Color of the opening")
    
    pgn_set_parser = pgn_command_subparsers.add_parser("set", help="Set PGN")
    pgn_set_parser.add_argument("opening", type=str, help="Name of the opening")
    pgn_set_parser.add_argument("color", type=str, choices=["w", "b"], help="Color of the opening")
    pgn_set_parser.add_argument("pgn", type=str, help="PGN")
    
    args = parser.parse_args()
    args.func(args)