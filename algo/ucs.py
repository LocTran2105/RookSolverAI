"""
Thuật toán UCS (Uniform Cost Search) để giải bài toán 8 Rooks
"""
from typing import List, Tuple, Optional
from queue import PriorityQueue
import time

class UCSSolver:
    def __init__(self, n: int = 8):
        self.n = n
        self.steps = 0
        self.time_taken = 0
        self.total_cost = 0
        
    def is_safe(self, board: List[int], row: int, col: int) -> bool:
        """Kiểm tra xem có thể đặt quân xe tại vị trí (row, col) không"""
        for i in range(row):
            if board[i] == col:
                return False
        return True
    
    def solve(self, callback=None, first_position=None) -> Tuple[Optional[List[int]], int, float, float]:
        """
        Giải bài toán 8 Rooks bằng UCS
        Returns: (solution, steps, time_taken, total_cost)
        """
        start_time = time.time()
        self.steps = 0
        
        if first_position:
            first_row, first_col = first_position
            initial_board = [first_col]
            initial_row = first_row + 1
            initial_cost = 1
        else:
            initial_board = []
            initial_row = 0
            initial_cost = 0
        
        prio_queue = PriorityQueue()
        prio_queue.put((initial_cost, initial_row, initial_board))
        
        while not prio_queue.empty():
            cost, row, curr_board = prio_queue.get()
            self.steps += 1
            self.total_cost = cost
            
            if callback:
                callback(curr_board, self.steps)
            
            if row == self.n:
                self.time_taken = time.time() - start_time
                return curr_board, self.steps, self.time_taken, self.total_cost
            
            for col in range(self.n):
                if self.is_safe(curr_board, row, col):
                    new_board = curr_board + [col]
                    prio_queue.put((cost + 1, row + 1, new_board))
        
        self.time_taken = time.time() - start_time
        return None, self.steps, self.time_taken, self.total_cost
