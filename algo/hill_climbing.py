"""
Thuật toán Hill Climbing để giải bài toán 8 Rooks
"""
from typing import List, Tuple, Optional
import random
import time

class HillClimbingSolver:
    def __init__(self, n: int = 8):
        self.n = n
        self.steps = 0
        self.time_taken = 0
        
    def create_individual(self, first_position=None) -> List[int]:
        """Tạo trạng thái ngẫu nhiên"""
        board = [-1] * self.n
        
        if first_position:
            first_row, first_col = first_position
            board[first_row] = first_col
        
        for row in range(self.n):
            if board[row] == -1:
                board[row] = random.randint(0, self.n - 1)
        
        return board
    
    def fitness(self, board: List[int]) -> int:
        """Hàm fitness (đánh giá chất lượng)"""
        conflicts = 0
        for col in range(self.n):
            count = sum(1 for row in range(self.n) if board[row] == col)
            if count > 1:
                conflicts += (count - 1)
        return self.n - conflicts
    
    def solve(self, callback=None, first_position=None) -> Tuple[Optional[List[int]], int, float]:
        """
        Giải bài toán 8 Rooks bằng Hill Climbing
        Returns: (solution, steps, time_taken)
        """
        start_time = time.time()
        self.steps = 0
        
        current = self.create_individual(first_position)
        
        while True:
            neighbors = []
            
            for row in range(self.n):
                # Không thay đổi vị trí first_position
                if first_position and row == first_position[0]:
                    continue
                
                for col in range(self.n):
                    if current[row] == col:
                        continue
                    
                    new_board = current[:]
                    new_board[row] = col
                    neighbors.append(new_board)
            
            if not neighbors:
                break
            
            best = max(neighbors, key=lambda x: self.fitness(x))
            self.steps += 1
            
            if callback and self.steps % 10 == 0:
                callback(best, self.steps)
            
            if self.fitness(best) <= self.fitness(current):
                self.time_taken = time.time() - start_time
                return current, self.steps, self.time_taken
            
            current = best
            
            if self.fitness(current) == self.n:
                self.time_taken = time.time() - start_time
                return current, self.steps, self.time_taken
        
        self.time_taken = time.time() - start_time
        return current, self.steps, self.time_taken
