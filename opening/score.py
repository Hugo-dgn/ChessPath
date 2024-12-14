def depthScore(node):
    links = node.children
    scores  = [(depth(link.end), link.move) for link in links]
    return scores

def successRateScore(node):
    links = node.children
    scores = [(_min_success_rate(link, []), link.move) for link in links]
    return scores

def visitScore(node):
    links = node.children
    scores = [(link.visits, link.move) for link in links]
    return scores

def agrregationScore(node):
    depth_scores = depthScore(node)
    success_rate_scores = successRateScore(node)
    visit_scores = visitScore(node)
    
    scores = []
    for depth_score, success_rate_score, visit_score in zip(depth_scores, success_rate_scores, visit_scores):
        score = (depth_score[0] + (success_rate_score[0] * visit_score[0] + 1e-3), depth_score[1])
        scores.append(score)
    return scores

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
        next_link_success_rate = min(next_link_success_rate, _min_success_rate(child_link, visited_node + [link.up]))
    
    return link.get_success_rate() * next_link_success_rate