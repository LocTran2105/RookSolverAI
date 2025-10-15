import time

class Minimax:
    def __init__(self, n=8):
        self.n = n
        self.steps = 0
        self.callback = None
    
    def is_safe(self, board, row, col):
        """Check if placing a rook at (row, col) is safe"""
        for i in range(self.n):
            if board[i] == -1:
                continue
            # Check same column or diagonal
            if board[i] == col or abs(board[i] - col) == abs(i - row):
                return False
        return True
    
    def minimax_search(self, board, row):
        """
        Minimax-style search for placing rooks
        Returns True if solution found, False otherwise
        """
        self.steps += 1
        
        print(f"[v0] Minimax search at row={row}, board={board}, steps={self.steps}")
        
        # Base case: all rows filled
        if row >= self.n:
            print(f"[v0] All rows filled! Solution found: {board}")
            return True
        
        # If this row already has a rook (from first_position), skip it
        if board[row] != -1:
            print(f"[v0] Row {row} already has rook at col {board[row]}, skipping")
            return self.minimax_search(board, row + 1)
        
        # Try each column for this row
        for col in range(self.n):
            print(f"[v0] Trying row={row}, col={col}")
            
            if self.is_safe(board, row, col):
                # Place rook
                board[row] = col
                print(f"[v0] Placed rook at ({row}, {col}), board={board}")
                
                if self.callback:
                    self.callback(board[:], self.steps)
                    time.sleep(0.05)  # 50ms delay to see the visualization
                
                # Recursively try to place remaining rooks
                if self.minimax_search(board, row + 1):
                    return True
                
                # Backtrack
                print(f"[v0] Backtracking from row={row}, col={col}")
                board[row] = -1
                
                if self.callback:
                    self.callback(board[:], self.steps)
                    time.sleep(0.05)
        
        # No valid placement found for this row
        print(f"[v0] No valid placement for row={row}")
        return False
    
    def solve(self, callback=None, first_position=None):
        """
        Solve 8 Rooks problem using Minimax-style search
        
        Args:
            callback: Function to call for UI updates
            first_position: Tuple (row, col) for first rook placement
        
        Returns:
            (solution, steps, time_taken)
        """
        print(f"[v0] ===== ADVERSARIAL SOLVER STARTED =====")
        print(f"[v0] First position: {first_position}")
        
        start_time = time.time()
        self.steps = 0
        self.callback = callback
        
        board = [-1] * self.n
        
        if first_position:
            row, col = first_position
            board[row] = col
            self.steps = 1
            
            print(f"[v0] Placed first rook at ({row}, {col})")
            
            if callback:
                callback(board[:], self.steps)
                time.sleep(0.1)
        
        print(f"[v0] Starting minimax search from row 0")
        success = self.minimax_search(board, 0)
        
        end_time = time.time()
        time_taken = end_time - start_time
        
        print(f"[v0] Minimax completed. Success: {success}, Solution: {board}, Steps: {self.steps}, Time: {time_taken:.3f}s")
        
        if success and all(x != -1 for x in board):
            return board, self.steps, time_taken
        else:
            return None, self.steps, time_taken
