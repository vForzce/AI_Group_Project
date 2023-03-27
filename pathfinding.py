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

def h(p, goal):
	x1, y1 = p
	x2, y2 = goal
	return abs(x1 - x2) + abs(y1 - y2)