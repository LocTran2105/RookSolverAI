"""
Beam Search Solver for 8 Rooks Problem
"""
import time
import random

class BeamSearchSolver:
    def __init__(self, n=8, beam_width=10):
        self.n = n
        self.beam_width = beam_width
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
    
    def generate_neighbors(self, board):
        """Generate neighbor states by moving rooks to different columns"""
        neighbors = []
        for row in range(self.n):
            for col in range(self.n):
                if board[row] != col:
                    neighbor = board[:]
                    neighbor[row] = col
                    neighbors.append(neighbor)
        return neighbors
    
    def solve(self, callback=None, first_position=None):
        """
        Solve 8 Rooks problem using Beam Search
        Returns: (solution, steps, time_taken, cost)
        """
        self.callback = callback
        self.steps = 0
        start_time = time.time()
        
        # Initialize starting board
        if first_position:
            row, col = first_position
            start_board = [-1] * self.n
            start_board[row] = col
            start_board = self.normalize_board(start_board)
        else:
            start_board = [random.randrange(self.n) for _ in range(self.n)]
        
        beam = [start_board]
        best_board = start_board[:]
        best_cost = self.calculate_conflicts(best_board)
        
        max_iterations = 2000
        iteration = 0
        
        while iteration < max_iterations and best_cost > 0:
            candidates = []
            
            # Generate neighbors for all states in beam
            for board in beam:
                neighbors = self.generate_neighbors(board)
                candidates.extend(neighbors)
            
            # Sort by cost and keep best beam_width states
            candidates.sort(key=lambda b: self.calculate_conflicts(b))
            
            # Remove duplicates
            seen = set()
            new_beam = []
            for board in candidates:
                key = tuple(board)
                if key not in seen:
                    seen.add(key)
                    new_beam.append(board)
                    if len(new_beam) >= self.beam_width:
                        break
            
            if not new_beam:
                break
            
            beam = new_beam
            
            # Update best solution
            for board in beam:
                cost = self.calculate_conflicts(board)
                self.steps += 1
                
                if callback and self.steps % 10 == 0:
                    callback(board, self.steps)
                
                if cost < best_cost:
                    best_board = board[:]
                    best_cost = cost
            
            iteration += 1
        
        time_taken = time.time() - start_time
        
        if best_cost == 0:
            return best_board, self.steps, time_taken, best_cost
        else:
            return None, self.steps, time_taken, best_cost
