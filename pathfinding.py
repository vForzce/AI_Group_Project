from collections import deque

def bfs(start, goal, graph):
    queue = deque([start])
    visited = {start: None}

    while queue:
        cur_node = queue.popleft()
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
                
    return queue, visited

def dfs(start, goal, graph):
    queue = deque([start])
    visited = {start: None}

    while queue:
        cur_node = queue.pop()
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in reversed(next_nodes):
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
                
    return queue, visited

def h(p, goal, weight):
    h = 0
    x1, y1 = p
    x2, y2 = goal

    for y in range(min(y1, y2) + 1, max(y1, y2) + 1):
        h += weight[(max(x1, x2), y)]
    for x in range(min(x1, x2) + 1, max(x1, x2) + 1):
        h += weight[(x, min(y1, y2))]
    # print(p, goal, h)
    return h

def heu(p, goal, weight, visited):
    h = 0
    curr = goal
    
    while curr != p and curr in visited:
        h += weight[curr]
        curr = visited[curr]
    
    return h

def ucs(start, goal, graph, weight):
    queue = [[0, start]]
    visited = {start: None}

    while queue:
        queue = sorted(queue, key=lambda x: x[0])
        cur_node = queue.pop(0)
        tup = cur_node[1]
        if tup == goal:
            break

        next_nodes = graph[tup]
        for next_node in next_nodes:
            if next_node not in visited:
                cost = cur_node[0] + weight[next_node]
                queue.append([cost, next_node])
                visited[next_node] = tup
   
    return deque([item[1] for item in queue]), visited

def greedy(start, goal, graph, weight):
    queue = [[h(start, goal, weight), start]]
    visited = {start: None}

    while queue:
        queue = sorted(queue, key=lambda x: x[0])
        cur_node = queue.pop(0)[1]
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append([h(next_node, goal, weight), next_node])
                visited[next_node] = cur_node
                
    return deque([item[1] for item in queue]), visited

def astar(start, goal, graph, weight):
    queue = [[h(start, goal, weight), start]]
    visited = {start: None}

    while queue:
        queue = sorted(queue, key=lambda x: x[0])
        # print(queue)
        # print()
        cur_node = queue.pop(0)
        cur_tup = cur_node[1]
        if cur_tup == goal:
            break

        next_nodes = graph[cur_tup]
        _, curr_visited = ucs(cur_tup, goal, graph, weight)
        for next_node in next_nodes:
            if next_node not in visited:
                _, next_visited = ucs(next_node, goal, graph, weight)
                cost = cur_node[0] - heu(cur_tup, goal, weight, curr_visited) \
                                    + weight[next_node] + heu(next_node, goal, weight, next_visited)
                queue.append([cost, next_node])
                visited[next_node] = cur_tup
                
    return deque([item[1] for item in queue]), visited