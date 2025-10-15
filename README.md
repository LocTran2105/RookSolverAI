
---

## ⚙️ Nhóm 1: **Thuật toán Tìm kiếm Mù (Uninformed Search)**

### 🔹 BFS (Breadth-First Search)
- Duyệt theo tầng, lần lượt đặt Xe vào từng hàng.
- Đảm bảo nghiệm đầu tiên tìm được là **nghiệm tối ưu** (ít bước nhất).  
- Nhược điểm: tốn bộ nhớ lớn khi không gian trạng thái lớn.

### 🔹 DFS (Depth-First Search)
- Đặt Xe từng hàng và đi sâu hết một nhánh trước khi quay lui.
- Dễ cài đặt, tiết kiệm bộ nhớ nhưng có thể đi sai hướng lâu.

### 🔹 DLS (Depth-Limited Search)
- Giới hạn độ sâu của DFS, chỉ mở rộng đến hàng `k` nhất định.
- Tránh lặp vô hạn nhưng có thể bỏ sót nghiệm.

### 🔹 IDS (Iterative Deepening Search)
- Kết hợp BFS và DFS bằng cách tăng dần giới hạn độ sâu.
- Hiệu quả hơn BFS, ít tốn bộ nhớ hơn.

### 🔹 UCS (Uniform Cost Search)
- Mở rộng nút có **chi phí nhỏ nhất** (ví dụ: số xung đột giữa các Xe).
- Đảm bảo nghiệm tối ưu nếu chi phí xác định đúng.

---

## 🎯 Nhóm 2: **Thuật toán Tìm kiếm Có Thông tin (Informed Search)**

### 🔹 Greedy Best-First Search
- Chỉ xét **hàm heuristic h(n)**: số lượng Xe đang xung đột.
- Luôn chọn trạng thái "ít xung đột nhất" để mở rộng.
- Nhanh nhưng dễ mắc kẹt tại nghiệm cục bộ.

### 🔹 A* (A-Star Search)
- Kết hợp `f(n) = g(n) + h(n)`:
  - `g(n)`: số Xe đã đặt.
  - `h(n)`: số Xe xung đột còn lại.
- Hiệu quả và tìm được nghiệm tối ưu nếu heuristic phù hợp.

---

## 🔄 Nhóm 3: **Thuật toán Tối ưu Cục bộ (Local Search)**

### 🔹 Hill Climbing
- Bắt đầu từ vị trí ngẫu nhiên.
- Dịch chuyển từng Xe sao cho giảm dần xung đột.
- Dễ mắc kẹt ở cực trị cục bộ.

### 🔹 Simulated Annealing (SA)
- Giống Hill Climbing nhưng có **xác suất chấp nhận trạng thái xấu tạm thời** để thoát cực trị cục bộ.

### 🔹 Beam Search
- Giữ lại **k trạng thái tốt nhất** ở mỗi bước thay vì chỉ một.
- Cân bằng giữa tìm kiếm toàn cục và cục bộ.

### 🔹 Genetic Algorithm
- Dùng **quần thể các lời giải (các bàn cờ)**.
- Thực hiện **lai ghép, đột biến** để sinh ra thế hệ mới.
- Mạnh mẽ với không gian tìm kiếm lớn.

---

## 🌍 Nhóm 4: **Môi trường Phức tạp (Complex Environment)**

### 🔹 AND-OR Search
- Dùng khi có **sự lựa chọn của đối thủ hoặc nhiều khả năng xảy ra**.
- Trong bài toán 8 Xe, có thể mô phỏng tình huống ràng buộc logic (ví dụ: Xe A buộc Xe B phải di chuyển sang hướng khác).

### 🔹 Partially Observable Search
- Môi trường **không quan sát đầy đủ**, ví dụ: chỉ biết một phần bàn cờ.
- Xe phải dự đoán vị trí có thể đặt dựa vào thông tin nhìn thấy.

### 🔹 Belief-State Search
- Mỗi trạng thái là một **tập hợp các khả năng có thể xảy ra**.
- Dùng để mô phỏng tìm kiếm trong không chắc chắn (ví dụ: ẩn vị trí cấm).

---

## 🧩 Nhóm 5: **Bài toán Ràng buộc (Constraint Satisfaction Problem - CSP)**

### 🔹 Backtracking
- Đặt Xe từng bước, nếu xung đột → quay lui.
- Đơn giản, hiệu quả cho các bài toán có ràng buộc mạnh.

### 🔹 Forward Checking
- Khi đặt một Xe, loại bỏ các vị trí không hợp lệ của Xe tiếp theo.
- Giảm đáng kể số lần backtrack.

### 🔹 AC-3 (Arc Consistency)
- Duy trì **tính nhất quán trên các cung (Xi, Xj)**.
- Loại bỏ giá trị vi phạm ràng buộc trước khi thử nghiệm.

---

## ⚔️ Nhóm 6: **Tìm kiếm Đối kháng (Adversarial Search)**

### 🔹 Minimax
- Mô phỏng tình huống **hai người chơi đối kháng**, ví dụ:
  - Người chơi A đặt Xe.
  - Người chơi B cố gắng phá bố cục (thêm chướng ngại hoặc cấm vị trí).
- Minimax chọn nước đi tối ưu theo logic “tốt nhất trong trường hợp xấu nhất”.

### 🔹 Alpha-Beta Pruning
- Cải tiến Minimax bằng cách **cắt tỉa** những nhánh không cần thiết.
- Giúp tăng tốc độ tìm kiếm đáng kể mà vẫn cho cùng kết quả.

---

## 📊 Thông số thống kê

Khi chạy mỗi thuật toán, hệ thống sẽ hiển thị:
- ⏱️ **Thời gian thực thi**
- 🌿 **Số nút mở rộng**
- 🧮 **Độ sâu tìm được**
- ♟️ **Số xung đột (nếu có)**
- ✅ **Trạng thái cuối cùng của bàn cờ**

---

## 💻 Công nghệ sử dụng
- Python 3.x  
- Tkinter (GUI)  
- Threading (chạy song song giao diện và thuật toán)  
- Matplotlib / Pillow (hiển thị ảnh bàn cờ, tùy chọn)

---

## 🚀 Cách chạy dự án

```bash
git clone https://github.com/LocTran2105/RookSolverAI.git
cd RookSolverAI
python main.py
