def depthScore(node):
    links = node.children
    next_link = max(links, key=lambda link: depth(link.end))
    next_move = next_link.move
    return next_move

def depth(node):
    return _depth(node, [])
    
def _depth(node, visited_node):
    for other in visited_node:
        if node is other:
            return -1
        
    if len(node.children) == 0:
        return 0
    
    child_links = node.children
    next_node_depth = 0
    for child_link in child_links:
        next_node = child_link.end
        next_node_depth = max(next_node_depth, _depth(next_node, visited_node + [node]))
    
    return 1 + next_node_depth
    