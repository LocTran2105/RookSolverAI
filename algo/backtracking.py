"""
Backtracking algorithm for 8 Rooks problem
Classic CSP approach - place rooks row by row and backtrack on conflicts
"""
import time

class BacktrackingSolver:
    def __init__(self, n=8):
        self.n = n
        self.steps = 0
    
    def is_safe(self, board, row, col):
        """Check if placing a rook at (row, col) is safe"""
        # Check column
        for i in range(row):
            if board[i] == col:
                return False
        
        # Check diagonals
        for i in range(row):
            if abs(board[i] - col) == abs(i - row):
                return False
        
        return True
    
    def backtrack(self, board, row, callback=None):
        """Backtracking algorithm"""
        if row == self.n:
            return True
        
        for col in range(self.n):
            if self.is_safe(board, row, col):
                board[row] = col
                self.steps += 1
                
                if callback:
                    callback(board[:row+1], self.steps)
                
                if self.backtrack(board, row + 1, callback):
                    return True
                
                board[row] = -1
        
        return False
    
    def solve(self, callback=None, first_position=None):
        """
        Solve 8 Rooks problem using Backtracking
        
        Args:
            callback: Function to call for UI updates
            first_position: Tuple (row, col) for first rook placement
        
        Returns:
            (solution, steps, time_taken)
        """
        start_time = time.time()
        self.steps = 0
        
        board = [-1] * self.n
        
        if first_position:
            row, col = first_position
            board[row] = col
            self.steps = 1
            
            if callback:
                callback([col], self.steps)
            
            # Try to complete the solution
            if row == 0:
                # First rook is in row 0, continue from row 1
                success = self.backtrack(board, 1, callback)
            else:
                # First rook is not in row 0, need to fill row 0 first
                # Then continue with remaining rows
                temp_board = [-1] * self.n
                temp_board[row] = col
                
                # Fill rows before first_position
                def backtrack_before(r):
                    if r == row:
                        # Now fill rows after first_position
                        for i in range(row + 1, self.n):
                            found = False
                            for c in range(self.n):
                                if self.is_safe(temp_board, i, c):
                                    temp_board[i] = c
                                    self.steps += 1
                                    if callback:
                                        callback([x for x in temp_board if x != -1], self.steps)
                                    found = True
                                    break
                            if not found:
                                return False
                        return True
                    
                    for c in range(self.n):
                        if self.is_safe(temp_board, r, c):
                            temp_board[r] = c
                            self.steps += 1
                            if callback:
                                callback([x for x in temp_board if x != -1], self.steps)
                            
                            if backtrack_before(r + 1):
                                return True
                            
                            temp_board[r] = -1
                    
                    return False
                
                success = backtrack_before(0)
                board = temp_board
        else:
            success = self.backtrack(board, 0, callback)
        
        end_time = time.time()
        time_taken = end_time - start_time
        
        if success:
            return board, self.steps, time_taken
        else:
            return None, self.steps, time_taken
