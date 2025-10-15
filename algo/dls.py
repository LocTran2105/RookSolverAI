"""
Depth Limited Search (DLS) Solver for 8 Rooks Problem
"""
import time

class DLSSolver:
    def __init__(self, n=8):
        self.n = n
        self.steps = 0
        self.callback = None
    
    def is_safe(self, board, row, col):
        """Check if placing a rook at (row, col) is safe"""
        for r in range(row):
            if board[r] == col:
                return False
        return True
    
    def solve_recursive(self, board, row, depth, limit):
        """Recursive DLS helper"""
        if row == self.n:
            return board[:]
        
        if depth == limit:
            return None
        
        for col in range(self.n):
            if self.is_safe(board, row, col):
                board[row] = col
                self.steps += 1
                
                if self.callback:
                    self.callback(board[:], self.steps)
                
                result = self.solve_recursive(board, row + 1, depth + 1, limit)
                if result:
                    return result
                
                board[row] = -1
        
        return None
    
    def solve(self, callback=None, first_position=None):
        """
        Solve 8 Rooks problem using DLS
        Returns: (solution, steps, time_taken)
        """
        self.callback = callback
        self.steps = 0
        start_time = time.time()
        
        board = [-1] * self.n
        start_row = 0
        
        if first_position:
            row, col = first_position
            board[row] = col
            start_row = row + 1
            self.steps = 1
            if callback:
                callback(board[:], self.steps)
        
        # Try with increasing depth limits
        for limit in range(self.n, self.n * 2):
            result = self.solve_recursive(board[:], start_row, 0, limit)
            if result:
                time_taken = time.time() - start_time
                return result, self.steps, time_taken
        
        time_taken = time.time() - start_time
        return None, self.steps, time_taken
