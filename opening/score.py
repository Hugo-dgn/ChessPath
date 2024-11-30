import numpy as np

def depthScore(node):
    links = node.children
    next_link = max(links, key=lambda link: depth(link.end))
    next_move = next_link.move
    return next_move

def successRateScore(node):
    links = node.children
    scores = np.array([_min_success_rate(link, []) for link in links])
    visits = np.array([link.visits for link in links])
    worst_link = np.min(scores)
    
    candidates = scores == worst_link
    visits[~candidates] = max(visits) + 1
    
    next_link_index = np.argmin(visits)
    next_link = links[next_link_index]
    
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

def _min_success_rate(link, visited_node):
    for other in visited_node:
        if link.up is other:
            return -1
    node = link.end
    if len(node.children) == 0:
        return link.get_success_rate()
    
    child_links = node.children
    next_link_success_rate = 1
    for child_link in child_links:
        next_node = child_link.end
        next_link_success_rate = min(next_link_success_rate, _min_success_rate(child_link, visited_node + [link.up]))
    
    return link.get_success_rate() * next_link_success_rate