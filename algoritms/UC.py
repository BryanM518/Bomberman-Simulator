import heapq
from collections import deque
from agents.metal import metal
from agents.grass import grass

def find_path(grid, start, goal):
    # Cola de prioridad donde cada entrada es (costo acumulado, posición)
    queue = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    visited = set()
    counter = 0

    while queue:
        current_cost, current = heapq.heappop(queue)

        if current == goal:
            return reconstruct_path(came_from, current)

        visited.add(current)

        agents_in_cell = grid.get_cell_list_contents([current])
        for agent in agents_in_cell:
            if isinstance(agent, grass):
                agent.label = counter
                counter += 1

        possible_steps = grid.get_neighborhood(current, moore=False, include_center=False)
        for next_pos in possible_steps:
            if (next_pos[1] == current[1]):
                new_cost = current_cost + 40
            elif (next_pos[0] == current[0]):
                new_cost = current_cost + 1
            if next_pos not in visited and is_accessible(grid, next_pos):
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    heapq.heappush(queue, (new_cost, next_pos))
                    came_from[next_pos] = current
            
            print(heapq)

    return None

def is_accessible(grid, position):
    # Verifica si la celda está vacía o no contiene una pared
    agent = grid.get_cell_list_contents([position])
    return all(not isinstance(a, metal) for a in agent)

def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path[1:]  # Devuelve el camino, excluyendo el nodo inicial