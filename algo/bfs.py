"""
Thuật toán BFS (Breadth-First Search) để giải bài toán 8 Rooks
"""
from collections import deque
from typing import List, Tuple, Optional
import time

class BFSSolver:
    def __init__(self, n: int = 8):
        self.n = n
        self.solutions = []
        self.steps = 0
        self.time_taken = 0
        
    def is_safe(self, board: List[int], row: int, col: int) -> bool:
        """
        Kiểm tra xem có thể đặt quân xe tại vị trí (row, col) không
        board[i] = j nghĩa là quân xe ở hàng i, cột j
        
        Đối với quân XE: chỉ cần kiểm tra cùng cột (không cần kiểm tra đường chéo)
        """
        for i in range(row):
            # Kiểm tra cùng cột
            if board[i] == col:
                return False
        return True
    
    def solve(self, callback=None, first_position=None) -> Tuple[Optional[List[int]], int, float]:
        """
        Giải bài toán 8 Rooks bằng BFS
        Args:
            callback: Hàm callback để cập nhật UI
            first_position: Tuple (row, col) vị trí quân xe đầu tiên do người dùng đặt
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
        
        queue = deque([(initial_board, initial_row)])
        
        while queue:
            board, row = queue.popleft()
            self.steps += 1
            
            if callback:
                callback(board, self.steps)
            
            if row == self.n:
                self.time_taken = time.time() - start_time
                return board, self.steps, self.time_taken
            
            for col in range(self.n):
                if self.is_safe(board, row, col):
                    new_board = board + [col]
                    queue.append((new_board, row + 1))
        
        self.time_taken = time.time() - start_time
        return None, self.steps, self.time_taken
    
    def get_board_state(self, solution: List[int]) -> List[List[int]]:
        """
        Chuyển đổi solution thành ma trận 2D để hiển thị
        """
        board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        for row, col in enumerate(solution):
            board[row][col] = 1
        return board
