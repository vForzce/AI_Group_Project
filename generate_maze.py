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
    graph = {}
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if not col:
                graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(grid, x, y)
    return grid, graph

def draw_mouse_cursor():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE, y // TILE
    pg.draw.rect(sc, pg.Color('red'), get_rect(grid_x, grid_y))

def draw_grid(grid):
    # fill screen
    sc.fill(pg.Color('black'))
    # draw grid
    [[pg.draw.rect(sc, pg.Color('darkorange'), get_rect(x, y), border_radius=TILE // 5)
      for x, col in enumerate(row) if col] for y, row in enumerate(grid)]


RES = WIDTH, HEIGHT = 902, 602
TILE = 30
cols, rows = WIDTH // TILE, HEIGHT // TILE

pg.init()
sc = pg.display.set_mode(RES)
clock = pg.time.Clock()

# grid
grid = [[1 if random() < 0.2 else 0 for _ in range(cols)] for _ in range(rows)]
# dict of adjacency lists
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(grid, x, y)

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
    path_head, path_segment = goal, goal
    while path_segment and path_segment in visited:
        pg.draw.rect(sc, pg.Color('white'), get_rect(*path_segment), TILE, border_radius=TILE // 3)
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
                grid, graph = new_grid(rows, cols)
                queue = deque([start])
                visited = {start: None}
                draw_grid(grid)
                
            if event.key == pg.K_d:
                if mouse_pos and not grid[mouse_pos[1]][mouse_pos[0]]:
                    queue, visited = pathfinding.dfs(start, mouse_pos, graph)
                    goal = mouse_pos

            if event.key == pg.K_b:
                if mouse_pos and not grid[mouse_pos[1]][mouse_pos[0]]:
                    queue, visited = pathfinding.bfs(start, mouse_pos, graph)
                    goal = mouse_pos    

    pg.display.flip()
    clock.tick(30)