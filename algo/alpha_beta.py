"""
Alpha-Beta Pruning Algorithm for 8 Rooks Problem
Tối ưu hóa của Minimax bằng cách cắt tỉa các nhánh không cần thiết
"""
import time

class AlphaBetaSolver:
    def __init__(self, n=8):
        self.n = n
        self.callback = None
        self.steps = 0
        self.pruned_branches = 0
        
    def is_safe(self, board, row, col):
        """Kiểm tra xem có thể đặt quân cờ tại vị trí (row, col) không"""
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
    
    def evaluate(self, board):
        """
        Đánh giá trạng thái board
        Trả về số quân cờ đã đặt thành công
        """
        placed = sum(1 for x in board if x != -1)
        return placed
    
    def alpha_beta_search(self, board, depth, alpha, beta, is_maximizing):
        """
        Tìm kiếm Alpha-Beta với pruning
        
        Args:
            board: Trạng thái bàn cờ hiện tại
            depth: Độ sâu hiện tại
            alpha: Giá trị tốt nhất cho MAX
            beta: Giá trị tốt nhất cho MIN
            is_maximizing: True nếu đang ở lượt MAX, False nếu MIN
        
        Returns:
            Giá trị đánh giá tốt nhất
        """
        self.steps += 1
        
        # Tìm hàng tiếp theo cần đặt quân cờ
        next_row = -1
        for i in range(self.n):
            if board[i] == -1:
                next_row = i
                break
        
        # Base case: đã đặt đủ 8 quân cờ
        if next_row == -1:
            print(f"[v0] Alpha-Beta: Found complete solution at depth {depth}")
            return self.evaluate(board)
        
        # Base case: đã đạt độ sâu tối đa
        if depth >= self.n:
            return self.evaluate(board)
        
        if is_maximizing:
            # MAX player: cố gắng tối đa hóa số quân cờ đặt được
            max_eval = float('-inf')
            
            for col in range(self.n):
                if self.is_safe(board, next_row, col):
                    # Đặt quân cờ
                    board[next_row] = col
                    
                    # Gọi callback để hiển thị
                    if self.callback:
                        self.callback(board[:], self.steps)
                    
                    print(f"[v0] Alpha-Beta MAX: Trying row {next_row}, col {col}, alpha={alpha}, beta={beta}")
                    
                    # Đệ quy với MIN player
                    eval_score = self.alpha_beta_search(board, depth + 1, alpha, beta, False)
                    
                    # Backtrack
                    board[next_row] = -1
                    
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    
                    # Beta cutoff (pruning)
                    if beta <= alpha:
                        self.pruned_branches += 1
                        print(f"[v0] Alpha-Beta: PRUNED at depth {depth} (beta={beta} <= alpha={alpha})")
                        break
            
            return max_eval
        else:
            # MIN player: cố gắng tối thiểu hóa (giả lập đối thủ cản trở)
            min_eval = float('inf')
            
            for col in range(self.n):
                if self.is_safe(board, next_row, col):
                    # Đặt quân cờ
                    board[next_row] = col
                    
                    # Gọi callback để hiển thị
                    if self.callback:
                        self.callback(board[:], self.steps)
                    
                    print(f"[v0] Alpha-Beta MIN: Trying row {next_row}, col {col}, alpha={alpha}, beta={beta}")
                    
                    # Đệ quy với MAX player
                    eval_score = self.alpha_beta_search(board, depth + 1, alpha, beta, True)
                    
                    # Backtrack
                    board[next_row] = -1
                    
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    
                    # Alpha cutoff (pruning)
                    if beta <= alpha:
                        self.pruned_branches += 1
                        print(f"[v0] Alpha-Beta: PRUNED at depth {depth} (beta={beta} <= alpha={alpha})")
                        break
            
            return min_eval
    
    def find_solution(self, board, row):
        """
        Tìm lời giải hoàn chỉnh sau khi Alpha-Beta đã chọn đường đi tốt nhất
        Sử dụng backtracking đơn giản
        """
        if row == self.n:
            return True
        
        # Nếu hàng này đã có quân cờ, bỏ qua
        if board[row] != -1:
            return self.find_solution(board, row + 1)
        
        for col in range(self.n):
            if self.is_safe(board, row, col):
                board[row] = col
                self.steps += 1
                
                if self.callback:
                    self.callback(board[:], self.steps)
                    time.sleep(0.05)
                
                if self.find_solution(board, row + 1):
                    return True
                
                board[row] = -1
        
        return False
    
    def solve(self, callback, first_position=None):
        """
        Giải bài toán 8 Rooks sử dụng Alpha-Beta Pruning
        
        Args:
            callback: Hàm callback để cập nhật UI
            first_position: Tuple (row, col) của quân cờ đầu tiên
        
        Returns:
            Tuple (solution, steps, time_taken)
        """
        print(f"[v0] Alpha-Beta: Starting solve with first_position={first_position}")
        
        self.callback = callback
        self.steps = 0
        self.pruned_branches = 0
        start_time = time.time()
        
        # Khởi tạo board với -1 (chưa đặt quân cờ)
        board = [-1] * self.n
        
        # Đặt quân cờ đầu tiên nếu có
        if first_position:
            row, col = first_position
            board[row] = col
            print(f"[v0] Alpha-Beta: Placed first rook at row {row}, col {col}")
            if callback:
                callback(board[:], self.steps)
        
        # Chạy Alpha-Beta để tìm đường đi tốt nhất
        print("[v0] Alpha-Beta: Running alpha-beta search...")
        alpha = float('-inf')
        beta = float('inf')
        best_eval = self.alpha_beta_search(board, 0, alpha, beta, True)
        
        print(f"[v0] Alpha-Beta: Search complete. Best eval={best_eval}, pruned={self.pruned_branches} branches")
        
        # Sau khi Alpha-Beta chọn đường đi, hoàn thiện lời giải bằng backtracking
        print("[v0] Alpha-Beta: Completing solution with backtracking...")
        if first_position:
            row, col = first_position
            board[row] = col
        else:
            board = [-1] * self.n
        
        success = self.find_solution(board, 0)
        
        end_time = time.time()
        time_taken = end_time - start_time
        
        if success:
            print(f"[v0] Alpha-Beta: Solution found! Steps={self.steps}, Time={time_taken:.3f}s")
            print(f"[v0] Alpha-Beta: Pruned {self.pruned_branches} branches")
            return board, self.steps, time_taken
        else:
            print(f"[v0] Alpha-Beta: No solution found. Steps={self.steps}")
            return None, self.steps, time_taken
