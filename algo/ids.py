"""
Thuật toán IDS (Iterative Deepening Search) để giải bài toán 8 Rooks
"""
from typing import List, Tuple, Optional
import time

class IDSSolver:
    def __init__(self, n: int = 8):
        self.n = n
        self.steps = 0
        self.time_taken = 0
        
    def is_safe(self, board: List[int], row: int, col: int) -> bool:
        """Kiểm tra xem có thể đặt quân xe tại vị trí (row, col) không"""
        for i in range(row):
            if board[i] == col:
                return False
        return True
    
    def dfs_limited(self, board: List[int], row: int, depth_limit: int, callback=None) -> Optional[List[int]]:
        """DFS với giới hạn độ sâu"""
        self.steps += 1
        
        if callback:
            callback(board, self.steps)
        
        if row == self.n:
            return board
        
        if row >= depth_limit:
            return None
        
        for col in range(self.n):
            if self.is_safe(board, row, col):
                result = self.dfs_limited(board + [col], row + 1, depth_limit, callback)
                if result:
                    return result
        
        return None
    
    def solve(self, callback=None, first_position=None) -> Tuple[Optional[List[int]], int, float]:
        """
        Giải bài toán 8 Rooks bằng IDS
        Returns: (solution, steps, time_taken)
        """
        start_time = time.time()
        self.steps = 0
        
        if first_position:
            first_row, first_col = first_position
            initial_board = [first_col]
            initial_row = first_row + 1
        else:
            initial_board = []
            initial_row = 0
        
        depth_limit = initial_row
        while depth_limit <= self.n:
            result = self.dfs_limited(initial_board, initial_row, depth_limit, callback)
            if result:
                self.time_taken = time.time() - start_time
                return result, self.steps, self.time_taken
            depth_limit += 1
        
        self.time_taken = time.time() - start_time
        return None, self.steps, self.time_taken
