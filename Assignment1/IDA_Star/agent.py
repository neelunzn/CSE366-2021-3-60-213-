import pygame
import heapq
from collections import deque

class Agent(pygame.sprite.Sprite):
    def __init__(self, environment, grid_size):
        super().__init__()
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill((0, 0, 255)) 
        self.rect = self.image.get_rect()
        self.grid_size = grid_size
        self.environment = environment
        self.position = [0, 0] 
        self.rect.topleft = (0, 0)
        self.task_completed = 0
        self.completed_tasks = []
        self.path = []  
        self.moving = False  
        self.task_costs = {}  
        self.total_path_cost = 0
        self.current_path_cost = 0

    def move(self):
        if self.path:
            next_position = self.path.pop(0)
            self.position = list(next_position)
            self.rect.topleft = (self.position[0] * self.grid_size, self.position[1] * self.grid_size)
            self.check_task_completion()
        else:
            self.moving = False  

    
    def find_nearest_task(self):
        nearest_task = None
        shortest_path = None
        for task_position in self.environment.task_locations.keys():
            path = self.find_path_to(task_position)
            if path:
                if not shortest_path or len(path) < len(shortest_path):
                    shortest_path = path
                    nearest_task = task_position
        if shortest_path:
            self.path = shortest_path[1:] 
            self.current_path_cost = len(shortest_path) - 1 
            self.moving = True

    def check_task_completion(self):
        position_tuple = tuple(self.position)
        if position_tuple in self.environment.task_locations:
            task_number = self.environment.task_locations.pop(position_tuple)
            self.task_completed += 1
 
            self.task_costs[task_number] = self.current_path_cost
            self.total_path_cost += self.current_path_cost
            
            self.completed_tasks.append(task_number)

    def find_path_to(self, target):
        start = tuple(self.position)
        goal = target
        
        def ida_star_search(path, g, cost_limit):
            current = path[-1]
            
            f = g + self.manhattan_distance(current, goal)

            if f > cost_limit:
                return False, f
            
            if current == goal:
                return path, None
            
            next_limit = float('inf')
            
            for neighbor in self.get_neighbors(*current):
                if neighbor in path:
                    continue
                
                path.append(neighbor)
                
                result, new_limit = ida_star_search(path, g + 1, cost_limit)
                
                if result is not False:
                    return result, None
                
                next_limit = min(next_limit, new_limit)
                
                path.pop()
            
            return False, next_limit
        
        cost_limit = self.manhattan_distance(start, goal)
        
        path = [start]
        
        while True:
            result, next_limit = ida_star_search(path, 0, cost_limit)
            if result is not False:
                return result
            
            if next_limit == float('inf'):
                return None

            cost_limit = next_limit

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def get_neighbors(self, x, y):
        neighbors = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny):
                neighbors.append((nx, ny))
        return neighbors