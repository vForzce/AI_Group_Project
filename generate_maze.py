import pygame as pg
import pathfinding
from random import random
from collections import deque

def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2

def get_next_nodes(grid, x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    ways = [0, -1], [-1, 0], [0, 1], [1, 0]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]

def new_grid(rows, cols):
    grid = [[1 if random() < 0.2 else 0 for _ in range(cols)] for _ in range(rows)]
    grid[0][0] = 0
    graph = {}
    weight = {}
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if not col:
                graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(grid, x, y)
                weight[(x, y)] = (y // 4) + 1
    weight[(0, 0)] = 0
    return grid, graph, weight

def draw_mouse_cursor():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE, y // TILE
    pg.draw.rect(sc, pg.Color('red'), get_rect(grid_x, grid_y))

def draw_grid(grid):
    # fill screen
    sc.fill(pg.Color(80, 80, 80))
    pg.draw.rect(sc, pg.Color(60, 60, 60), pg.Rect(0, 120, 902, 120))
    pg.draw.rect(sc, pg.Color(40, 40, 40), pg.Rect(0, 240, 902, 120))
    pg.draw.rect(sc, pg.Color(20, 20, 20), pg.Rect(0, 360, 902, 120))
    pg.draw.rect(sc, pg.Color(0, 0, 0), pg.Rect(0, 480, 902, 120))
    # draw grid
    [[pg.draw.rect(sc, pg.Color('darkorange'), get_rect(x, y), border_radius=TILE // 5)
      for x, col in enumerate(row) if col] for y, row in enumerate(grid)]


RES = WIDTH, HEIGHT = 902, 602
TILE = 30
cols, rows = WIDTH // TILE, HEIGHT // TILE

pg.init()
sc = pg.display.set_mode(RES)
clock = pg.time.Clock()
pg.display.set_caption("Path Finding Algorithms")

# grid
grid = [[1 if random() < 0.2 else 0 for _ in range(cols)] for _ in range(rows)]
# weight = [[(row // 4) + 1 for _ in range(cols)] for row in range(rows)]
weight = {}
grid[0][0] = 0
# dict of adjacency lists
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(grid, x, y)
            weight[(x, y)] = (y // 4) + 1
weight[(0, 0)] = 0

# pathfinding settings
start = (0, 0)
mouse_pos = (0, 0)
goal = start
queue = deque([start])
visited = {start: None}

while True:
    draw_grid(grid)
    draw_mouse_cursor()
    
    # draw visited nodes
    [pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(x, y)) for x, y in visited]
    [pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(x, y)) for x, y in queue]

    # draw click
    pg.draw.rect(sc, pg.Color('magenta'), get_rect(mouse_pos[0], mouse_pos[1]), border_radius=TILE // 3)
    
    # draw path
    total_weight = 0
    path_head, path_segment = goal, goal
    while path_segment and path_segment in visited:
        pg.draw.rect(sc, pg.Color('white'), get_rect(*path_segment), TILE, border_radius=TILE // 3)
        total_weight += weight[path_segment]
        path_segment = visited[path_segment]
        

    pg.draw.rect(sc, pg.Color('blue'), get_rect(*start), border_radius=TILE // 3)
    pg.draw.rect(sc, pg.Color('magenta'), get_rect(*path_head), border_radius=TILE // 3)

    # interaction
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
            
        if pg.mouse.get_pressed()[0]: # LEFT
            x, y = pg.mouse.get_pos()
            grid_x, grid_y = x // TILE, y // TILE
            mouse_pos = (grid_x, grid_y)
            
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                pg.display.set_caption('Path Finding Algorithms')
                grid, graph, weight = new_grid(rows, cols)
                queue = deque([start])
                visited = {start: None}
                draw_grid(grid)
                
            if event.key == pg.K_d:
                if mouse_pos and not grid[mouse_pos[1]][mouse_pos[0]]:
                    pg.display.set_caption('Depth First Search')
                    queue, visited = pathfinding.dfs(start, mouse_pos, graph)
                    goal = mouse_pos

            if event.key == pg.K_b:
                if mouse_pos and not grid[mouse_pos[1]][mouse_pos[0]]:
                    pg.display.set_caption('Breath First Search')
                    queue, visited = pathfinding.bfs(start, mouse_pos, graph)
                    goal = mouse_pos
            
            if event.key == pg.K_u:
                if mouse_pos and not grid[mouse_pos[1]][mouse_pos[0]]:
                    pg.display.set_caption('Uniform Cost Search')
                    queue, visited = pathfinding.ucs(start, mouse_pos, graph, weight)
                    goal = mouse_pos
                    
            if event.key == pg.K_g:
                if mouse_pos and not grid[mouse_pos[1]][mouse_pos[0]]:
                    pg.display.set_caption('Greedy Search')
                    queue, visited = pathfinding.greedy(start, mouse_pos, graph)
                    goal = mouse_pos
            
            if event.key == pg.K_a:
                if mouse_pos and not grid[mouse_pos[1]][mouse_pos[0]]:
                    pg.display.set_caption('A* Search')
                    queue, visited = pathfinding.astar(start, mouse_pos, graph, weight)
                    goal = mouse_pos
                    
            if event.key == pg.K_w:
                print(total_weight)

    pg.display.flip()
    clock.tick(30)