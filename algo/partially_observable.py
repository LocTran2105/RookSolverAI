"""
Partially Observable Search Solver for 8 Rooks Problem

Trong môi trường partially observable, agent không thể quan sát toàn bộ trạng thái.
Agent phải duy trì belief state (tập hợp các trạng thái có thể) và lập kế hoạch dựa trên thông tin không đầy đủ.

Cách tiếp cận:
1. Agent chỉ có thể "nhìn thấy" một số hàng/cột giới hạn tại một thời điểm
2. Duy trì belief state về vị trí có thể đặt quân cờ
3. Sử dụng sensing actions để thu thập thêm thông tin
4. Lập kế hoạch dựa trên belief state hiện tại
"""

import time
from collections import deque

class PartiallyObservableSolver:
    def __init__(self, n=8):
        self.n = n
        self.steps = 0
        self.callback = None
        self.observation_window = 3  # Agent chỉ có thể quan sát 3 hàng/cột tại một thời điểm
        
    def is_safe(self, board, row, col):
        """Kiểm tra xem có thể đặt quân cờ tại (row, col) không"""
        for i in range(self.n):
            if board[i] == -1:
                continue
            # Kiểm tra cùng cột
            if board[i] == col:
                return False
            # Kiểm tra đường chéo
            if abs(board[i] - col) == abs(i - row):
                return False
        return True
    
    def get_observable_region(self, board, current_row):
        """
        Trả về vùng quan sát được từ current_row
        Agent chỉ có thể nhìn thấy observation_window hàng xung quanh
        """
        start_row = max(0, current_row - self.observation_window // 2)
        end_row = min(self.n, start_row + self.observation_window)
        
        observable = []
        for i in range(start_row, end_row):
            observable.append((i, board[i]))
        
        return observable
    
    def compute_belief_state(self, board, row):
        """
        Tính toán belief state: tập hợp các cột có thể đặt quân cờ
        dựa trên thông tin quan sát được
        """
        observable = self.get_observable_region(board, row)
        
        print(f"[v0] Computing belief state for row {row}")
        print(f"[v0] Observable region: {observable}")
        
        # Tính toán các cột có thể dựa trên thông tin quan sát được
        possible_cols = []
        for col in range(self.n):
            # Kiểm tra với các quân cờ trong vùng quan sát
            safe = True
            for obs_row, obs_col in observable:
                if obs_col == -1:
                    continue
                # Kiểm tra xung đột với quân cờ đã biết
                if obs_col == col or abs(obs_col - col) == abs(obs_row - row):
                    safe = False
                    break
            
            if safe:
                possible_cols.append(col)
        
        print(f"[v0] Possible columns for row {row}: {possible_cols}")
        return possible_cols
    
    def sense_and_update(self, board, row):
        """
        Thực hiện sensing action để cập nhật belief state
        Mô phỏng việc agent "nhìn" vào board để thu thập thông tin
        """
        self.steps += 1
        
        # Mô phỏng sensing: kiểm tra toàn bộ board để cập nhật belief
        # (trong thực tế, đây sẽ là một action có chi phí)
        conflicts = []
        for i in range(self.n):
            if board[i] != -1:
                for j in range(i + 1, self.n):
                    if board[j] != -1:
                        if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                            conflicts.append((i, j))
        
        return conflicts
    
    def solve_with_partial_info(self, board, row):
        """
        Giải bài toán với thông tin không đầy đủ
        Sử dụng belief state và sensing actions
        """
        # Base case: đã đặt đủ 8 quân cờ
        if row >= self.n:
            return True
        
        # Nếu hàng này đã có quân cờ (first position), bỏ qua
        if board[row] != -1:
            return self.solve_with_partial_info(board, row + 1)
        
        print(f"[v0] Solving row {row} with partial observability")
        
        # Tính toán belief state: các cột có thể đặt
        possible_cols = self.compute_belief_state(board, row)
        
        # Nếu không có cột nào khả dụng trong belief state, thực hiện sensing
        if not possible_cols:
            print(f"[v0] No possible columns in belief state, performing sensing...")
            conflicts = self.sense_and_update(board, row)
            print(f"[v0] Detected conflicts: {conflicts}")
            return False
        
        # Thử từng cột trong belief state
        for col in possible_cols:
            # Kiểm tra an toàn với toàn bộ board (sau khi sensing)
            if self.is_safe(board, row, col):
                print(f"[v0] Placing rook at ({row}, {col}) based on belief state")
                
                # Đặt quân cờ
                board[row] = col
                self.steps += 1
                
                # Cập nhật UI
                if self.callback:
                    self.callback(board[:], self.steps)
                    time.sleep(0.05)  # Delay để thấy quá trình
                
                # Thực hiện sensing để xác nhận
                conflicts = self.sense_and_update(board, row)
                if conflicts:
                    print(f"[v0] Sensing detected conflicts: {conflicts}, backtracking...")
                    board[row] = -1
                    if self.callback:
                        self.callback(board[:], self.steps)
                        time.sleep(0.03)
                    continue
                
                # Đệ quy
                if self.solve_with_partial_info(board, row + 1):
                    return True
                
                # Backtrack
                print(f"[v0] Backtracking from ({row}, {col})")
                board[row] = -1
                self.steps += 1
                if self.callback:
                    self.callback(board[:], self.steps)
                    time.sleep(0.03)
        
        return False
    
    def solve(self, callback, first_position=None):
        """
        Giải bài toán 8 Rooks với Partially Observable Search
        
        Args:
            callback: Hàm callback để cập nhật UI
            first_position: Tuple (row, col) của quân cờ đầu tiên
            
        Returns:
            Tuple (solution, steps, time_taken)
        """
        print("[v0] Starting Partially Observable Search")
        print(f"[v0] Observation window: {self.observation_window} rows/cols")
        
        self.callback = callback
        self.steps = 0
        
        start_time = time.time()
        
        # Khởi tạo board với -1 (chưa đặt)
        board = [-1] * self.n
        
        # Đặt quân cờ đầu tiên nếu có
        if first_position:
            row, col = first_position
            board[row] = col
            print(f"[v0] First position: ({row}, {col})")
            if callback:
                callback(board[:], self.steps)
        
        # Giải bài toán với thông tin không đầy đủ
        success = self.solve_with_partial_info(board, 0)
        
        end_time = time.time()
        time_taken = end_time - start_time
        
        if success:
            print(f"[v0] Solution found! Steps: {self.steps}, Time: {time_taken:.3f}s")
            print(f"[v0] Solution: {board}")
            return board, self.steps, time_taken
        else:
            print(f"[v0] No solution found. Steps: {self.steps}, Time: {time_taken:.3f}s")
            return [], self.steps, time_taken
