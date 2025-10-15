"""
Simulated Annealing Solver for 8 Rooks Problem
"""
import time
import random
import math

class SimulatedAnnealingSolver:
    def __init__(self, n=8, initial_temp=5.0, cooling_rate=0.9995):
        self.n = n
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.steps = 0
        self.callback = None
    
    def calculate_conflicts(self, board):
        """Calculate number of conflicts (rooks attacking each other)"""
        conflicts = 0
        col_counts = {}
        
        for row in range(self.n):
            col = board[row]
            if col >= 0:
                col_counts[col] = col_counts.get(col, 0) + 1
        
        for count in col_counts.values():
            if count > 1:
                conflicts += (count - 1)
        
        return conflicts
    
    def normalize_board(self, board):
        """Fill empty positions with random columns"""
        result = board[:]
        for i in range(self.n):
            if result[i] < 0:
                result[i] = random.randrange(self.n)
        return result
    
    def generate_neighbor(self, board):
        """Generate a neighbor state"""
        neighbor = board[:]
        
        if random.random() < 0.6:
            # Swap two rows
            i, j = random.sample(range(self.n), 2)
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        else:
            # Move one rook to random column
            i = random.randrange(self.n)
            neighbor[i] = random.randrange(self.n)
        
        return neighbor
    
    def solve(self, callback=None, first_position=None):
        """
        Solve 8 Rooks problem using Simulated Annealing
        Returns: (solution, steps, time_taken, cost)
        """
        self.callback = callback
        self.steps = 0
        start_time = time.time()
        
        # Initialize starting board
        if first_position:
            row, col = first_position
            current_board = [-1] * self.n
            current_board[row] = col
            current_board = self.normalize_board(current_board)
        else:
            current_board = [random.randrange(self.n) for _ in range(self.n)]
        
        best_board = current_board[:]
        best_cost = self.calculate_conflicts(best_board)
        
        temperature = self.initial_temp
        max_steps = 20000
        
        while self.steps < max_steps and best_cost > 0:
            neighbor = self.generate_neighbor(current_board)
            
            current_cost = self.calculate_conflicts(current_board)
            neighbor_cost = self.calculate_conflicts(neighbor)
            
            delta = neighbor_cost - current_cost
            
            # Accept neighbor if better or with probability based on temperature
            if delta <= 0 or random.random() < math.exp(-delta / temperature):
                current_board = neighbor
                current_cost = neighbor_cost
                
                if current_cost < best_cost:
                    best_board = current_board[:]
                    best_cost = current_cost
            
            self.steps += 1
            
            if callback and self.steps % 100 == 0:
                callback(best_board, self.steps)
            
            # Cool down
            temperature *= self.cooling_rate
        
        time_taken = time.time() - start_time
        
        if best_cost == 0:
            return best_board, self.steps, time_taken, best_cost
        else:
            return None, self.steps, time_taken, best_cost
