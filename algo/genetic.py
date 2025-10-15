"""
Thuật toán Genetic Algorithm để giải bài toán 8 Rooks
"""
from typing import List, Tuple, Optional
import random
import time

class GeneticSolver:
    def __init__(self, n: int = 8):
        self.n = n
        self.steps = 0
        self.time_taken = 0
        self.pop_size = 50
        self.generations = 300
        
    def create_individual(self, first_position=None) -> List[int]:
        """Tạo cá thể trong quần thể ban đầu"""
        board = [-1] * self.n
        
        if first_position:
            first_row, first_col = first_position
            board[first_row] = first_col
        
        for row in range(self.n):
            if board[row] == -1:
                board[row] = random.randint(0, self.n - 1)
        
        return board
    
    def fitness(self, board: List[int]) -> int:
        """Hàm fitness (đánh giá chất lượng) = số không tấn công"""
        conflicts = 0
        for col in range(self.n):
            count = sum(1 for row in range(self.n) if board[row] == col)
            if count > 1:
                conflicts += (count - 1)
        return self.n - conflicts
    
    def selection(self, pop: List[List[int]]) -> List[int]:
        """Chọn lọc (lấy 2 cha mẹ random và chọn tốt hơn)"""
        return max(random.sample(pop, 2), key=lambda x: self.fitness(x))
    
    def crossover(self, p1: List[int], p2: List[int], first_position=None) -> List[int]:
        """Lai tạo ra cá thể con"""
        point = random.randint(1, self.n - 1)
        child = p1[:point] + p2[point:]
        
        # Giữ nguyên vị trí first_position nếu có
        if first_position:
            first_row, first_col = first_position
            child[first_row] = first_col
        
        return child
    
    def mutate(self, board: List[int], first_position=None) -> List[int]:
        """Đột biến"""
        row = random.randint(0, self.n - 1)
        
        # Không đột biến vị trí first_position
        if first_position and row == first_position[0]:
            return board
        
        board[row] = random.randint(0, self.n - 1)
        return board
    
    def solve(self, callback=None, first_position=None) -> Tuple[Optional[List[int]], int, float]:
        """
        Giải bài toán 8 Rooks bằng Genetic Algorithm
        Returns: (solution, steps, time_taken)
        """
        start_time = time.time()
        self.steps = 0
        
        # Tạo quần thể ban đầu
        pop = [self.create_individual(first_position) for _ in range(self.pop_size)]
        
        for gen in range(self.generations):
            pop = sorted(pop, key=lambda x: self.fitness(x), reverse=True)
            
            if callback and gen % 10 == 0:
                callback(pop[0], gen)
            
            if self.fitness(pop[0]) == self.n:
                self.steps = gen
                self.time_taken = time.time() - start_time
                return pop[0], self.steps, self.time_taken
            
            new_pop = []
            for _ in range(self.pop_size // 2):
                p1, p2 = self.selection(pop), self.selection(pop)
                c1 = self.crossover(p1, p2, first_position)
                c2 = self.crossover(p2, p1, first_position)
                
                if random.random() < 0.2:
                    c1 = self.mutate(c1, first_position)
                if random.random() < 0.2:
                    c2 = self.mutate(c2, first_position)
                
                new_pop.extend([c1, c2])
            
            pop = new_pop
        
        self.steps = self.generations
        self.time_taken = time.time() - start_time
        return pop[0], self.steps, self.time_taken
