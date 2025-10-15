"""
Thuật toán A* Search để giải bài toán 8 Rooks
"""
from typing import List, Tuple, Optional
from queue import PriorityQueue
from copy import deepcopy
import time

class AStarSolver:
    def __init__(self, n: int = 8):
        self.n = n
        self.steps = 0
        self.time_taken = 0
        self.g_cost = 0  # Chi phí hiện tại
        self.h_cost = 0  # Chi phí ước tính
        self.f_cost = 0  # Tổng chi phí
        
    def is_safe(self, board: List[int], row: int, col: int) -> bool:
        """Kiểm tra xem có thể đặt quân xe tại vị trí (row, col) không"""
        for i in range(row):
            if board[i] == col:
                return False
        return True
    
    def h_cost_func(self, board: List[int]) -> int:
        """
        Hàm tính chi phí ước tính - heuristic
        Chi phí = số cột chưa bị chiếm
        """
        used_cols = set(board)
        return self.n - len(used_cols)
    
    def g_cost_func(self, board: List[int]) -> int:
        """
        Hàm tính chi phí hiện tại (từ trạng thái ban đầu đến trạng thái hiện tại)
        Chi phí = số quân đã đặt
        """
        return len(board)
    
    def f_cost_func(self, board: List[int]) -> int:
        """Tổng 2 chi phí: f(x) = g(x) + h(x)"""
        return self.g_cost_func(board) + self.h_cost_func(board)
    
    def solve(self, callback=None, first_position=None) -> Tuple[Optional[List[int]], int, float, int, int, int]:
        """
        Giải bài toán 8 Rooks bằng A*
        Returns: (solution, steps, time_taken, g_cost, h_cost, f_cost)
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
        
        prio_queue = PriorityQueue()
        prio_queue.put((self.f_cost_func(initial_board), initial_row, initial_board))
        
        while not prio_queue.empty():
            f_cost, row, curr_board = prio_queue.get()
            self.steps += 1
            
            # Cập nhật chi phí hiện tại
            self.g_cost = self.g_cost_func(curr_board)
            self.h_cost = self.h_cost_func(curr_board)
            self.f_cost = f_cost
            
            if callback:
                callback(curr_board, self.steps)
            
            if row == self.n:
                self.time_taken = time.time() - start_time
                return curr_board, self.steps, self.time_taken, self.g_cost, self.h_cost, self.f_cost
            
            for col in range(self.n):
                if self.is_safe(curr_board, row, col):
                    new_board = curr_board + [col]
                    prio_queue.put((self.f_cost_func(new_board), row + 1, new_board))
        
        self.time_taken = time.time() - start_time
        return None, self.steps, self.time_taken, self.g_cost, self.h_cost, self.f_cost
