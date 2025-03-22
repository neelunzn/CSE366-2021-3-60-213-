import pygame
import heapq
from collections import deque

class Agent(pygame.sprite.Sprite):
    def __init__(self, environment, grid_size):
        super().__init__()
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill((0, 0, 255))  # Agent color is blue
        self.rect = self.image.get_rect()
        self.grid_size = grid_size
        self.environment = environment
        self.position = [0, 0]  # Starting at the top-left corner of the grid
        self.rect.topleft = (0, 0)
        self.task_completed = 0
        self.completed_tasks = []
        self.path = []  # List of positions to follow
        self.moving = False  # Flag to indicate if the agent is moving
        self.task_costs = {}  # Dictionary to store the cost for each completed task
        self.total_path_cost = 0
        self.current_path_cost = 0
    def move(self):
        """Move the agent along the path."""
        if self.path:
            next_position = self.path.pop(0)
            self.position = list(next_position)
            self.rect.topleft = (self.position[0] * self.grid_size, self.position[1] * self.grid_size)
            self.check_task_completion()
        else:
            self.moving = False  # Stop moving when path is exhausted

    
    def find_nearest_task(self):
        """Find the nearest task based on the shortest path length using A*."""
        nearest_task = None
        shortest_path = None
        for task_position in self.environment.task_locations.keys():
            path = self.find_path_to(task_position)
            if path:
                if not shortest_path or len(path) < len(shortest_path):
                    shortest_path = path
                    nearest_task = task_position
        if shortest_path:
            self.path = shortest_path[1:]  # Exclude the current position
            self.current_path_cost = len(shortest_path) - 1  # Store the cost of this path
            self.moving = True

    def check_task_completion(self):
        """Check if the agent has reached a task location."""
        position_tuple = tuple(self.position)
        if position_tuple in self.environment.task_locations:
            task_number = self.environment.task_locations.pop(position_tuple)
            self.task_completed += 1
            
            # Store the cost for this task
            self.task_costs[task_number] = self.current_path_cost
            self.total_path_cost += self.current_path_cost
            
            self.completed_tasks.append(task_number)

    def find_path_to(self, target):
        """Find a path to the target position using IDA* algorithm."""
        start = tuple(self.position)
        goal = target
        
        # Helper function for the recursive IDA* search
        def ida_star_search(path, g, cost_limit):
            current = path[-1]
            
            # Calculate f-score (g + h)
            f = g + self.manhattan_distance(current, goal)
            
            # If f exceeds the cost limit, return the f as the next cost limit
            if f > cost_limit:
                return False, f
            
            # Goal reached
            if current == goal:
                return path, None
            
            next_limit = float('inf')
            
            # Check all neighbors
            for neighbor in self.get_neighbors(*current):
                # Skip if neighbor is already in path (avoid cycles)
                if neighbor in path:
                    continue
                
                # Add neighbor to path
                path.append(neighbor)
                
                # Recursive call
                result, new_limit = ida_star_search(path, g + 1, cost_limit)
                
                # If result is not False, we found a path to goal
                if result is not False:
                    return result, None
                
                # Update the next cost limit
                next_limit = min(next_limit, new_limit)
                
                # Remove neighbor from path (backtrack)
                path.pop()
            
            return False, next_limit
        
        # Initial cost limit based on heuristic
        cost_limit = self.manhattan_distance(start, goal)
        
        # Path so far
        path = [start]
        
        while True:
            # Search with current cost limit
            result, next_limit = ida_star_search(path, 0, cost_limit)
            
            # If result is not False, we found a path
            if result is not False:
                return result
            
            # If next_limit is infinity, no path exists
            if next_limit == float('inf'):
                return None
            
            # Update the cost limit for next iteration
            cost_limit = next_limit

    def manhattan_distance(self, pos1, pos2):
        """Calculate Manhattan distance between two positions."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def get_neighbors(self, x, y):
        """Get walkable neighboring positions."""
        neighbors = []
        directions = [("up", (0, -1)), ("down", (0, 1)), ("left", (-1, 0)), ("right", (1, 0))]
        for _, (dx, dy) in directions:
            nx, ny = x + dx, y + dy
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny):
                neighbors.append((nx, ny))
        return neighbors