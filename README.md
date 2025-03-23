# Grid-Based Pathfinding Simulation with A* and IDA* Algorithm

This repository (CSE366-2021-3-60-213) contains implementations of two advanced pathfinding algorithms—A* and IDA*—for grid-based robot navigation. The simulation demonstrates how these algorithms perform in environments with obstacles, allowing for a comparison of their efficiency, path quality, and computational characteristics.

# Introduction

This project implements a grid-based simulation where an autonomous agent navigates through a grid environment to complete tasks. The agent uses the A* and IDA* pathfinding algorithms to find the optimal path to each task location while avoiding barriers in the environment.

# Setup Instructions

# Requirements
  * Python 3.6 or later
  * Pygame library
    
# Installation

 1. Clone this repository to your local machine:
      git clone https://github.com/neelunzn/CSE366-2021-3-60-213-.git
    
 2. Navigate to the repository:
      cd CSE366-2021-3-60-213-

 3. Install required dependencies:
      pip install pygame

# A* Implementation

The A* algorithm uses a best-first search approach with an open list (priority queue) and a closed set to find the optimal path from start to goal. Key features of our implementation:
  * Completeness: A* is complete, meaning it will always find a solution if one exists.
  * Optimality: A* guarantees the shortest path when using an admissible heuristic.
  * Efficiency: A* is very efficient compared to uninformed search algorithms, especially with a good heuristic.

# IDA* Implementation

The IDA* algorithm uses iterative deepening with a depth-first search approach to find optimal paths while using less memory. Key features:
  * IDA Pathfinding*: Combines the memory efficiency of depth-first search with the optimality of A* search
  * Task Prioritization: Agent automatically finds and moves to the nearest available task
  * Task Completion Tracking: Records completed tasks and their associated costs
  * Obstacle Avoidance: Navigates around barriers in the environment

# Analysis and Observations

 1. Memory Usage:

    * A* maintains an open list and closed set, consuming more memory in large grids.

    * IDA* uses memory proportional to the path depth, making it more efficient for large grids.

 2. Speed:

    * A* generally finds paths faster in open environments.

    * IDA* may re-explore states, leading to slower performance in some cases.

    * In environments with many barriers, the performance difference between A* and IDA* is minimal.

  3. Path Quality:

    * Both algorithms produce optimal paths of the same length when using the same heuristic.

    * Path visualization confirms identical routes for the same start/goal configurations.

    * IDA* maintains consistent memory usage, unaffected by grid size.


    
