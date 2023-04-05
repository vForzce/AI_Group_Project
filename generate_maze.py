import pygame as pg
import pathfinding
from random import random
from collections import deque

# set bound
RES = WIDTH, HEIGHT = 900, 600
TILE = 30
cols, rows = WIDTH // TILE, HEIGHT // TILE

def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2

def get_next_nodes(grid, x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    ways = [0, -1], [-1, 0], [0, 1], [1, 0]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]

def new_grid(rows, cols, rand=True):
    # random grid
    grid = [[1 if random() < 0.2 else 0 for _ in range(cols)] for _ in range(rows)]
    grid[0][0] = 0
    for y in range(3):
        for x in range(cols - 3, cols):
            grid[y][x] = 1

    graph = {}
    weight = {}
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            weight[(x, y)] = ((y // 4) + 1) if rand else 1
            if not col:
                graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(grid, x, y)

    weight[(0, 0)] = 0
    return grid, graph, weight