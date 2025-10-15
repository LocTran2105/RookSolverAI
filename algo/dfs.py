"""
Thuật toán DFS (Depth-First Search) có tính chi phí để giải bài toán 8 Rooks
"""
from copy import deepcopy
import time

class DFSSolver:
    def __init__(self, n=8):
        self.n = n
        self.nodes_explored = 0
        self.total_cost = 0
        
    def hop_le(self, state, row, col):
        """Kiểm tra vị trí đặt có hợp lệ hay không"""
        # Kiểm tra cùng cột
        for r in range(self.n):
            if state[r][col] == 1:
                return False
        # Kiểm tra cùng hàng
        for c in range(self.n):
            if state[row][c] == 1:
                return False
        return True
    
    def tinh_chi_phi(self, state, row, col):
        """Tính chi phí khi đặt quân tại (row, col)"""
        cost = 1
        bi_chan = 0
        # Đếm ô bị chặn cùng cột
        for r in range(self.n):
            if state[r][col] == 0:
                bi_chan += 1
        # Đếm ô bị chặn cùng hàng
        for c in range(self.n):
            if state[row][c] == 0:
                bi_chan += 1
        cost += bi_chan / self.n
        return cost
    
    def sinh_trang_thai(self, state, row, current_cost):
        """Sinh các trạng thái kế tiếp hợp lệ"""
        trang_thai_moi = []
        for col in range(self.n):
            if self.hop_le(state, row, col):
                new_state = deepcopy(state)
                new_state[row][col] = 1
                cost = current_cost + self.tinh_chi_phi(state, row, col)
                trang_thai_moi.append((new_state, cost))
        return trang_thai_moi
    
    def state_to_solution(self, state):
        """Chuyển đổi state (ma trận) sang solution (list vị trí cột)"""
        solution = []
        for row in range(self.n):
            for col in range(self.n):
                if state[row][col] == 1:
                    solution.append(col)
                    break
        return solution
    
    def solve(self, update_callback=None, first_position=None):
        """
        Giải bài toán 8 Rooks bằng DFS có tính chi phí
        Args:
            update_callback: Hàm callback để cập nhật UI
            first_position: Tuple (row, col) vị trí quân xe đầu tiên do người dùng đặt
        Returns: (solution, nodes_explored, time_taken, total_cost)
        """
        start_time = time.time()
        self.nodes_explored = 0
        self.total_cost = 0
        
        initial_state = [[0] * self.n for _ in range(self.n)]
        initial_row = 0
        
        if first_position:
            first_row, first_col = first_position
            initial_state[first_row][first_col] = 1
            initial_row = first_row + 1
        
        stack = [(initial_state, initial_row, 0)]
        
        while stack:
            state, row, cost = stack.pop()
            self.nodes_explored += 1
            
            if update_callback and row > 0:
                current_solution = self.state_to_solution(state)
                update_callback(current_solution, self.nodes_explored)
            
            if row == self.n:
                self.total_cost = cost
                solution = self.state_to_solution(state)
                time_taken = time.time() - start_time
                return solution, self.nodes_explored, time_taken, self.total_cost
            
            for next_state, new_cost in self.sinh_trang_thai(state, row, cost):
                stack.append((next_state, row + 1, new_cost))
        
        time_taken = time.time() - start_time
        return None, self.nodes_explored, time_taken, 0
