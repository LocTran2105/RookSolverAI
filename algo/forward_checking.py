"""
Forward Checking algorithm for 8 Rooks problem
Backtracking with domain pruning - check future domains after each placement
"""
import time

class ForwardCheckingSolver:
    def __init__(self, n=8):
        self.n = n
        self.steps = 0
    
    def get_domain(self, board, row, domains):
        """Get valid domain for a row given current board state"""
        valid = []
        for col in range(self.n):
            if col not in domains[row]:
                continue
            
            safe = True
            for i in range(row):
                if board[i] == col or abs(board[i] - col) == abs(i - row):
                    safe = False
                    break
            
            if safe:
                valid.append(col)
        
        return valid
    
    def forward_check(self, board, row, col, domains):
        """
        Check if placing rook at (row, col) leaves valid domains for future rows
        Returns pruned domains or None if any domain becomes empty
        """
        new_domains = [d.copy() for d in domains]
        
        # Remove col from all future rows
        for future_row in range(row + 1, self.n):
            if col in new_domains[future_row]:
                new_domains[future_row].remove(col)
            
            # Remove diagonal conflicts
            for c in list(new_domains[future_row]):
                if abs(c - col) == abs(future_row - row):
                    new_domains[future_row].remove(c)
            
            # Check if domain is empty
            if len(new_domains[future_row]) == 0:
                return None
        
        return new_domains
    
    def backtrack_fc(self, board, row, domains, callback=None):
        """Backtracking with forward checking"""
        if row == self.n:
            return True
        
        valid_cols = self.get_domain(board, row, domains)
        
        for col in valid_cols:
            board[row] = col
            self.steps += 1
            
            if callback:
                callback(board[:row+1], self.steps)
            
            # Forward check
            new_domains = self.forward_check(board, row, col, domains)
            
            if new_domains is not None:
                if self.backtrack_fc(board, row + 1, new_domains, callback):
                    return True
            
            board[row] = -1
        
        return False
    
    def solve(self, callback=None, first_position=None):
        """
        Solve 8 Rooks problem using Forward Checking
        
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
            self.steps = 1
            
            # Update domains based on first position
            domains = self.forward_check(board, row, col, domains)
            
            if domains is None:
                # First position makes problem unsolvable
                end_time = time.time()
                return None, self.steps, end_time - start_time
            
            if callback:
                callback([col], self.steps)
            
            # Continue from next row
            if row < self.n - 1:
                success = self.backtrack_fc(board, row + 1, domains, callback)
            else:
                success = True
        else:
            success = self.backtrack_fc(board, 0, domains, callback)
        
        end_time = time.time()
        time_taken = end_time - start_time
        
        if success:
            return board, self.steps, time_taken
        else:
            return None, self.steps, time_taken
