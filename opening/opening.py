import chess
import chess.pgn
import io

from .node import Node

class Opening:
    
    def __init__(self, name : str, color : chess.Color, tree : Node) -> None:
        self.name = name
        self.color = color
        self.tree = tree
        self.cursor = tree
        self.board = chess.Board()
    
    def root(self) -> Node:
        self.cursor = self.tree
        self.board = chess.Board()
        return self.tree
    
    def line(self, moves : list) -> Node:
        self.root()
        for move in moves:
            flag = self.move(move)
            if not flag:
                raise ValueError("The move is not in the opening or is illegal.")
        return self.cursor

    def push(self, move : chess.Move) -> Node:
        if not self.board.is_legal(move):
            raise ValueError("The move is not legal.")
        self.board.push(move)
        self.cursor.add_child(move)
        self.cursor = self.cursor.push(move)
        return self.cursor

    def pop(self) -> Node:
        move = self.board.pop()
        self.cursor = self.cursor.back(move)
        self.cursor.delete_child(move)
        return self.cursor
    
    def next(self) -> list:
        return self.cursor.get_moves()
    
    def back(self) -> Node:
        move = self.board.pop()
        self.cursor = self.cursor.back(move)
        return self.cursor

    def move(self, move : chess.Move) -> Node:
        if not self.board.is_legal(move):
            raise ValueError("The move is not legal.")
        flag = move in self.cursor.get_moves()
        if flag:
            self.board.push(move)
            self.cursor = self.cursor.push(move)
        return flag
    
    def __eq__(self, other: object) -> bool:
        flag = self.name == other.name and self.color == other.color
        if not flag:
            return False
        stack = [self.tree]
        
        _buffer_cursor1 = self.cursor
        _buffer_cursor2 = other.cursor
        
        self.root()
        other.root()
        flag = True
        while len(stack) > 0 and flag:
            node = stack.pop()
            moves_1 = set(node.get_moves())
            moves_2 = set(other.cursor.get_moves())
            if moves_1 != moves_2:
                flag = False
            
            children = node.get_children()
            if children is not None:
                stack.extend(children)
        
        self.cursor = _buffer_cursor1
        other.cursor = _buffer_cursor2
        return flag
    
    def get_pgn(self):
        game = chess.pgn.Game()
        self.root()
        
        visited = []
        
        def aux(pgnNode, node):
            if node in visited:
                return
            visited.append(node)
            
            arrows = node.arrows_annotations
            pgnNode.set_arrows(arrows)
            
            for link in node.children:
                move = link.move
                child = link.end
                child_pgn = pgnNode.add_variation(move)
                aux(child_pgn, child)
        
        aux(game, self.tree)
        
        pgn = game.__str__().split("\n")[-1]
        
        return pgn
    
def from_pgn(name, color, pgn):
    tree = Node()
    opening = Opening(name, color, tree)
    pgn = io.StringIO(pgn)
    game = chess.pgn.read_game(pgn)
    
    def aux(pgnNode, node):
        arrows = pgnNode.arrows()
        node.arrows_annotations = arrows
        for child in pgnNode.variations:
            move = child.move
            leaf = node.add_child(move)
            aux(child, leaf)
    aux(game, opening.tree)
    
    return opening
