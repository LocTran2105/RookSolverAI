"""
AC3 (Arc Consistency 3) algorithm for 8 Rooks problem
Maintains arc consistency between all variables before search
"""
import time
from collections import deque

class AC3Solver:
    def __init__(self, n=8):
        self.n = n
        self.steps = 0
    
    def is_consistent(self, row1, col1, row2, col2):
        """Check if two rook placements are consistent (don't attack each other)"""
        if col1 == col2:
            return False
        if abs(col1 - col2) == abs(row1 - row2):
            return False
        return True
    
    def revise(self, domains, row1, row2):
        """
        Revise domain of row1 based on row2
        Returns True if domain was revised
        """
        revised = False
        
        for col1 in list(domains[row1]):
            # Check if there exists a value in row2's domain that is consistent
            consistent_exists = False
            for col2 in domains[row2]:
                if self.is_consistent(row1, col1, row2, col2):
                    consistent_exists = True
                    break
            
            # If no consistent value exists, remove col1 from domain
            if not consistent_exists:
                domains[row1].remove(col1)
                revised = True
        
        return revised
    
    def ac3(self, domains):
        """
        AC3 algorithm to enforce arc consistency
        Returns True if consistent, False if any domain becomes empty
        """
        # Create queue of all arcs
        queue = deque()
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    queue.append((i, j))
        
        while queue:
            row1, row2 = queue.popleft()
            self.steps += 1
            
            if self.revise(domains, row1, row2):
                if len(domains[row1]) == 0:
                    return False
                
                # Add all arcs (k, row1) where k != row1 and k != row2
                for k in range(self.n):
                    if k != row1 and k != row2:
                        queue.append((k, row1))
        
        return True
    
    def backtrack_ac3(self, board, row, domains, callback=None):
        """Backtracking with AC3"""
        if row == self.n:
            return True
        
        for col in sorted(domains[row]):
            board[row] = col
            self.steps += 1
            
            if callback:
                callback(board[:row+1], self.steps)
            
            # Create new domains for future rows
            new_domains = [d.copy() for d in domains]
            new_domains[row] = {col}
            
            # Run AC3 on remaining variables
            if self.ac3(new_domains):
                if self.backtrack_ac3(board, row + 1, new_domains, callback):
                    return True
            
            board[row] = -1
        
        return False
    
    def solve(self, callback=None, first_position=None):
        """
        Solve 8 Rooks problem using AC3
        
        Args:
            callback: Function to call for UI updates
            first_position: Tuple (row, col) for first rook placement
        
        Returns:
            (solution, steps, time_taken)
        """
        start_time = time.time()
        self.steps = 0
        
        board = [-1] * self.n
        domains = [set(range(self.n)) for _ in range(self.n)]
        
        if first_position:
            row, col = first_position
            board[row] = col
            domains[row] = {col}
            self.steps = 1
            
            # Run AC3 to propagate constraints
            if not self.ac3(domains):
                end_time = time.time()
                return None, self.steps, end_time - start_time
            
            if callback:
                callback([col], self.steps)
            
            # Continue from next row
            if row < self.n - 1:
                success = self.backtrack_ac3(board, row + 1, domains, callback)
            else:
                success = True
        else:
            # Run initial AC3
            self.ac3(domains)
            success = self.backtrack_ac3(board, 0, domains, callback)
        
        end_time = time.time()
        time_taken = end_time - start_time
        
        if success:
            return board, self.steps, time_taken
        else:
            return None, self.steps, time_taken
