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
        """Find a path to the target position using A* algorithm."""
        start = tuple(self.position)
        goal = target
        
        # Priority queue for open nodes
        # Format: (f_score, node_count, position)
        open_queue = [(0, 0, start)]
        open_set = {start}  # For faster lookup
        node_count = 1
        
        # For tracking progress
        came_from = {}
        
        # g_score: cost from start to current position
        g_score = {start: 0}
        
        while open_queue:
            # Get position with lowest f_score
            _, _, current = heapq.heappop(open_queue)
            
            if current in open_set:
                open_set.remove(current)
            else:
                continue  # Node was already processed
            
            # Goal reached
            if current == goal:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]  # Return reversed path
            
            # Check all neighbors
            for neighbor in self.get_neighbors(*current):
                # Distance from start to neighbor through current
                tentative_g_score = g_score[current] + 1
                
                # This path is better than any previous one
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f = tentative_g_score + self.manhattan_distance(neighbor, goal)
                    
                    if neighbor not in open_set:
                        heapq.heappush(open_queue, (f, node_count, neighbor))
                        open_set.add(neighbor)
                        node_count += 1  # Increment after pushing to queue
        
        # No path found
        return None

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