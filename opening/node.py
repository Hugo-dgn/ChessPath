import chess

import utils

class Node:
    
    def __init__(self) -> None:
        self.parents = []
        self.children = []
    
    def _add_child(self, move : chess.Move, leaf : 'Node') -> None:
        link = Link(move, self, leaf)
        self.children.append(link)
        leaf.parents.append(link)
    
    def add_child(self, move : chess.Move) -> 'Node':
        if move in self.get_moves():
            return

        leaf = Node()
        self._add_child(move, leaf)

        twin = _find_twin(self.root(), leaf)
        if twin is not None:
            leaf = twin
            self.children.pop()
            self._add_child(move, leaf)
        
        return leaf
    
    def delete_child(self, move : chess.Move) -> None:
        for link in self.children:
            if link.move == move:
                self.children.remove(link)
                link.end.parents.remove(link)
                return
    
    def is_child(self, node : 'Node') -> bool:
        for link in self.children:
            if link.end is node:
                return True
        return False
    
    def is_parent(self, node : 'Node') -> bool:
        for link in self.parents:
            if link.up is node:
                return True
        return False

    def get_children(self) -> list:
        children = []
        for link in self.children:
            children.append(link.end)
    
    def get_parents(self) -> list:
        parents = []
        for link in self.parents:
            parents.append(link.up)
    
    def push(self, move : chess.Move) -> 'Node':
        for link in self.children:
            if link.move == move:
                return link.end
        return None

    def back(self, move) -> 'Node':
        for link in self.parents:
            if link.move == move:
                return link.up
    
    def get_moves(self) -> list:
        return [link.move for link in self.children]
    
    def get_position(self) -> str:
        board = chess.Board()
        moves = []
        
        node = self
        while len(node.parents) > 0:
            link = node.parents[0]
            moves.insert(0, link.move)
            node = link.up
        
        for move in moves:
            board.push(move)
        
        return utils.get_position(board)

    def root(self) -> 'Node':
        node = self
        while len(node.parents) > 0:
            node = node.parents[0].up
        return node

    def __eq__(self, other):
        return self.get_position() == other.get_position()

class Link:
    
    def __init__(self, move : chess.Move, up : Node, down : Node) -> None:
        self.move = move
        self.up = up
        self.end = down
        self.visits = 0
        self.successes = 0
    
    def __eq__(self, other):
        return self.move == other.move

def _find_twin(root : Node, node : Node) -> Node:
    position = node.get_position()
    def aux(root, board):
        if root is not node and root.get_position() == position:
            return root
        for link in root.children:
            _board = board.copy()
            _board.push(link.move)
            result = aux(link.end, _board)
            if result:
                return result
        return None
    
    return aux(root, chess.Board())
        