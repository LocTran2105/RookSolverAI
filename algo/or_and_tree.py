"""
AND-OR Tree Search Algorithm for 8 Rooks Problem

AND-OR tree search is a planning algorithm where:
- OR nodes represent choices (which column to place a rook)
- AND nodes represent requirements (all constraints must be satisfied)

For the 8 Rooks problem:
- Each row is an OR node (choose one column from available options)
- The complete solution is an AND node (all rows must have valid placements)
"""

import time
from typing import List, Tuple, Optional, Callable

class ORAndTreeSolver:
    def __init__(self, n: int = 8):
        self.n = n
        self.nodes_explored = 0
        self.callback = None
        
    def is_safe(self, board: List[int], row: int, col: int) -> bool:
        """
        Kiểm tra xem có thể đặt quân cờ tại vị trí (row, col) không
        
        Args:
            board: Danh sách vị trí cột của các quân cờ đã đặt (board[i] = cột của quân cờ ở hàng i)
            row: Hàng cần kiểm tra
            col: Cột cần kiểm tra
            
        Returns:
            True nếu vị trí an toàn, False nếu không
        """
        # Kiểm tra với tất cả các quân cờ đã đặt
        for r in range(len(board)):
            # Bỏ qua các vị trí chưa đặt
            if board[r] == -1:
                continue
                
            # Kiểm tra cột
            if board[r] == col:
                return False
            
            # Kiểm tra đường chéo
            if abs(board[r] - col) == abs(r - row):
                return False
        
        return True
    
    def get_available_columns(self, board: List[int], row: int) -> List[int]:
        """
        Lấy danh sách các cột có thể đặt quân cờ cho hàng hiện tại (OR node)
        
        Args:
            board: Danh sách vị trí cột của các quân cờ đã đặt
            row: Hàng hiện tại
            
        Returns:
            Danh sách các cột có thể đặt
        """
        available = []
        for col in range(self.n):
            if self.is_safe(board, row, col):
                available.append(col)
        return available
    
    def and_node(self, board: List[int], row: int) -> bool:
        """
        AND node: Tất cả các ràng buộc phải được thỏa mãn
        Kiểm tra xem có thể hoàn thành bài toán từ trạng thái hiện tại không
        
        Args:
            board: Danh sách vị trí cột của các quân cờ đã đặt
            row: Hàng hiện tại
            
        Returns:
            True nếu tìm được lời giải, False nếu không
        """
        print(f"[v0] AND node: row={row}, board={board}")
        
        # Base case: Đã xử lý tất cả các hàng
        if row == self.n:
            print(f"[v0] Solution found! board={board}")
            return True
        
        # Nếu hàng này đã có quân cờ (từ first_position), bỏ qua
        if board[row] != -1:
            print(f"[v0] Row {row} already has rook at col {board[row]}, skipping")
            return self.and_node(board, row + 1)
        
        # Gọi OR node để chọn một cột cho hàng này
        return self.or_node(board, row)
    
    def or_node(self, board: List[int], row: int) -> bool:
        """
        OR node: Chọn một trong các lựa chọn có thể
        Thử đặt quân cờ vào các cột khả dụng
        
        Args:
            board: Danh sách vị trí cột của các quân cờ đã đặt
            row: Hàng hiện tại
            
        Returns:
            True nếu tìm được lời giải, False nếu không
        """
        # Lấy danh sách các cột có thể đặt (OR choices)
        available_cols = self.get_available_columns(board, row)
        
        print(f"[v0] OR node: row={row}, available_cols={available_cols}")
        
        # Nếu không có cột nào khả dụng, backtrack
        if not available_cols:
            print(f"[v0] No available columns for row {row}, backtracking")
            return False
        
        # Thử từng cột (OR node - chọn một trong các lựa chọn)
        for col in available_cols:
            self.nodes_explored += 1
            
            # Đặt quân cờ tại vị trí này
            board[row] = col
            
            print(f"[v0] Placed rook at ({row}, {col}), calling callback with board={board}")
            
            # Cập nhật UI nếu có callback - truyền toàn bộ board
            if self.callback:
                self.callback(board[:], self.nodes_explored)
            
            # Gọi AND node để kiểm tra xem có thể hoàn thành không
            if self.and_node(board, row + 1):
                return True
            
            # Backtrack: Bỏ quân cờ vừa đặt
            print(f"[v0] Backtracking from ({row}, {col})")
            board[row] = -1
        
        # Không tìm được lời giải từ các lựa chọn này
        return False
    
    def solve(self, callback: Optional[Callable] = None, 
              first_position: Optional[Tuple[int, int]] = None) -> Tuple[List[int], int, float]:
        """
        Giải bài toán 8 Rooks bằng AND-OR Tree Search
        
        Args:
            callback: Hàm callback để cập nhật UI
            first_position: Vị trí quân cờ đầu tiên (row, col)
            
        Returns:
            Tuple gồm (solution, nodes_explored, time_taken)
            - solution: Danh sách vị trí cột của các quân cờ
            - nodes_explored: Số node đã khám phá
            - time_taken: Thời gian thực hiện (giây)
        """
        print(f"[v0] Starting OR-AND Tree Search")
        print(f"[v0] First position: {first_position}")
        
        self.callback = callback
        self.nodes_explored = 0
        
        start_time = time.time()
        
        board = [-1] * self.n
        
        # Nếu có vị trí đầu tiên, đặt quân cờ tại đó
        if first_position:
            row, col = first_position
            board[row] = col
            print(f"[v0] Set first position: board={board}")
            
            # Cập nhật UI
            if callback:
                print(f"[v0] Calling callback with initial board")
                callback(board[:], self.nodes_explored)
        
        print(f"[v0] Starting AND node from row 0")
        success = self.and_node(board, 0)
        
        end_time = time.time()
        time_taken = end_time - start_time
        
        print(f"[v0] Search completed: success={success}, board={board}, nodes={self.nodes_explored}, time={time_taken:.3f}s")
        
        # Xử lý kết quả
        if success:
            return board, self.nodes_explored, time_taken
        else:
            # Không tìm được lời giải
            return [], self.nodes_explored, time_taken
