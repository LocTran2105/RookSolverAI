# RookSolverAI - Đặt 8 Quân Xe Bằng Trí Tuệ Nhân Tạo

## 1. Giới thiệu

RookSolverAI là một chương trình mô phỏng việc giải bài toán đặt 8 quân Xe (8 Rooks Problem) trên bàn cờ 8x8 bằng nhiều thuật toán trí tuệ nhân tạo (AI Search Algorithms).

**Mục tiêu:**  
Đặt 8 quân Xe lên bàn cờ sao cho không có hai quân nào tấn công nhau, tức là không có hai Xe nào cùng hàng hoặc cùng cột.

Chương trình cho phép lựa chọn thuật toán để giải, hiển thị quá trình tìm kiếm và các thông số như: thời gian chạy, số nút mở rộng, độ sâu và trạng thái bàn cờ cuối cùng.

---

## 2. Nhóm thuật toán Tìm kiếm Mù (Uninformed Search)

### Tổng quan

Các thuật toán tìm kiếm mù không sử dụng thông tin bổ sung về bài toán ngoài các trạng thái hợp lệ và mục tiêu. Chúng tìm kiếm một cách toàn diện nhưng không có định hướng.

### 2.1 BFS (Breadth-First Search)

**Mô tả:** Duyệt theo chiều rộng, lần lượt đặt Xe vào từng hàng, thử tất cả các khả năng ở mỗi tầng trước khi sang tầng sâu hơn.

<p align="center">
  <img src="gif/bfs.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>  
**Ưu điểm:** Luôn tìm được nghiệm tối ưu (nếu có) với số bước ít nhất.  
**Nhược điểm:** Tốn rất nhiều bộ nhớ do phải lưu toàn bộ trạng thái cùng mức.

**Áp dụng:** Trong bài toán 8 Xe, BFS lần lượt đặt từng Xe vào mỗi hàng và kiểm tra xem có xung đột hay không. Khi đủ 8 Xe, trạng thái được xem là lời giải.

---

### 2.2 DFS (Depth-First Search)

**Mô tả:** Duyệt theo chiều sâu, đặt Xe vào hàng đầu tiên và đi sâu xuống các hàng tiếp theo. Nếu phát hiện xung đột thì quay lui.

<p align="center">
  <img src="gif/dfs.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Ưu điểm:** Tiết kiệm bộ nhớ, dễ cài đặt.  
**Nhược điểm:** Có thể đi sai hướng và mắc kẹt trong nhánh không có nghiệm.

**Áp dụng:** DFS hữu ích khi cần tìm nhanh một lời giải mà không quan trọng tối ưu, nhưng không đảm bảo tìm được nghiệm tốt nhất.

---

### 2.3 DLS (Depth-Limited Search)

**Mô tả:** Giống DFS nhưng có giới hạn độ sâu.

<p align="center">
  <img src="gif/dls.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Ưu điểm:** Tránh việc đi sâu vô hạn trong không gian tìm kiếm.  
**Nhược điểm:** Nếu giới hạn độ sâu nhỏ hơn nghiệm, thuật toán sẽ không tìm thấy lời giải.

**Áp dụng:** DLS thích hợp khi biết trước giới hạn số Xe cần đặt.

---

### 2.4 IDS (Iterative Deepening Search)

**Mô tả:** Kết hợp BFS và DFS, bằng cách tăng dần giới hạn độ sâu trong mỗi vòng lặp.

<p align="center">
  <img src="gif/ids.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Ưu điểm:** Đảm bảo tìm được nghiệm tối ưu mà không tốn nhiều bộ nhớ như BFS.  
**Nhược điểm:** Phải duyệt lại nhiều lần các trạng thái ban đầu.

**Áp dụng:** IDS phù hợp cho bài toán có không gian tìm kiếm lớn, nhưng cần cân bằng giữa tốc độ và độ chính xác.

---

### 2.5 UCS (Uniform Cost Search)

**Mô tả:** Luôn mở rộng trạng thái có chi phí thấp nhất (ví dụ: số lượng xung đột giữa các Xe).

<p align="center">
  <img src="gif/ucs.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Ưu điểm:** Tìm được nghiệm có chi phí tối ưu.  
**Nhược điểm:** Cần xác định đúng hàm chi phí, tốn thời gian nếu không gian trạng thái lớn.

**Áp dụng:** Với 8 Xe, UCS mở rộng các bàn cờ ít xung đột hơn trước.

---

### Kết luận nhóm Uninformed Search

Nhóm thuật toán này phù hợp với việc **tìm lời giải chính xác**, đặc biệt trong bài toán có không gian nhỏ. Tuy nhiên, khi bàn cờ mở rộng (nhiều Xe hơn), chi phí thời gian và bộ nhớ trở nên lớn. BFS và IDS cho nghiệm tối ưu, còn DFS và DLS nhanh hơn nhưng có thể bỏ sót nghiệm.

---

## 3. Nhóm thuật toán Tìm kiếm Có Thông tin (Informed Search)

### Tổng quan

Các thuật toán này sử dụng hàm heuristic (ước lượng) để đánh giá mức độ “tốt” của trạng thái, giúp định hướng tìm kiếm hiệu quả hơn.

### 3.1 Greedy Best-First Search

**Mô tả:** Mở rộng trạng thái có giá trị heuristic nhỏ nhất, thường là số lượng Xe đang xung đột.

<p align="center">
  <img src="gif/greedy.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Ưu điểm:** Chạy nhanh, dễ cài đặt.  
**Nhược điểm:** Dễ mắc kẹt ở nghiệm cục bộ, không đảm bảo tối ưu.

**Áp dụng:** Greedy ưu tiên những bàn cờ có ít xung đột, giúp đạt kết quả nhanh trong nhiều trường hợp.

---

### 3.2 A\* (A-Star Search)

**Mô tả:** Kết hợp chi phí thực tế và ước lượng: f(n) = g(n) + h(n), trong đó:

- g(n): số Xe đã đặt hoặc chi phí thực tế.
- h(n): số xung đột còn lại cần giảm.  
 **Ưu điểm:** Tìm được nghiệm tối ưu nếu hàm heuristic là khả chấp (admissible).  
 **Nhược điểm:** Cần tính toán nhiều hơn, có thể tốn bộ nhớ.
<p align="center">
  <img src="gif/astar.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Áp dụng:** Trong bài toán 8 Xe, A\* định hướng tìm kiếm về các bàn cờ ít xung đột hơn, tránh việc duyệt mù như BFS.

---

### Kết luận nhóm Informed Search

Các thuật toán có thông tin mang lại **tốc độ và hiệu quả cao hơn**. A\* thường cho kết quả tốt nhất, trong khi Greedy thích hợp cho các trường hợp cần tốc độ cao mà không yêu cầu tối ưu tuyệt đối.

---

## 4. Nhóm thuật toán Tối ưu Cục bộ (Local Search)

### Tổng quan

Các thuật toán tối ưu cục bộ không tìm kiếm toàn bộ không gian mà chỉ tập trung cải thiện dần lời giải hiện tại. Chúng hữu ích trong không gian tìm kiếm rất lớn.

### 4.1 Hill Climbing

**Mô tả:** Bắt đầu từ một bàn cờ ngẫu nhiên, di chuyển từng Xe để giảm số xung đột.

<p align="center">
  <img src="gif/hill.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Ưu điểm:** Dễ cài đặt, tốc độ nhanh.  
**Nhược điểm:** Dễ mắc kẹt tại nghiệm cục bộ, không tìm được lời giải tốt hơn.

---

### 4.2 Simulated Annealing

**Mô tả:** Giống Hill Climbing nhưng đôi khi chấp nhận bước đi “xấu hơn” với xác suất nhất định để thoát khỏi cực trị cục bộ.

<p align="center">
  <img src="gif/sa.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Ưu điểm:** Có thể tìm được nghiệm tốt hơn so với Hill Climbing.  
**Nhược điểm:** Phụ thuộc nhiều vào tham số nhiệt độ và tốc độ giảm.

---

### 4.3 Beam Search

**Mô tả:** Giữ lại một số trạng thái tốt nhất (beam width) ở mỗi vòng để mở rộng tiếp.

<p align="center">
  <img src="gif/beam.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Ưu điểm:** Cân bằng giữa tốc độ và độ bao phủ không gian tìm kiếm.  
**Nhược điểm:** Có thể bỏ lỡ nghiệm tối ưu nếu beam quá nhỏ.

---

### 4.4 Genetic Algorithm

**Mô tả:** Biểu diễn bàn cờ dưới dạng nhiễm sắc thể, áp dụng phép lai và đột biến để tạo ra thế hệ mới.

<p align="center">
  <img src="gif/gene.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Ưu điểm:** Mạnh mẽ, có thể tìm nghiệm tốt trong không gian rất lớn.  
**Nhược điểm:** Cần nhiều tham số và có thể mất thời gian huấn luyện.

---

### Kết luận nhóm Local Search

Nhóm này phù hợp khi không gian tìm kiếm quá lớn để duyệt toàn bộ. Hill Climbing và Simulated Annealing dễ áp dụng, còn Genetic Algorithm mạnh hơn nhưng phức tạp hơn.

---

## 5. Nhóm thuật toán Môi trường Phức tạp (Complex Environment)

### Tổng quan

Nhóm này mô phỏng môi trường không chắc chắn hoặc có nhiều khả năng xảy ra, đòi hỏi mô hình hóa trạng thái niềm tin và logic.

### 5.1 AND-OR Search

**Mô tả:** Mô phỏng quá trình ra quyết định khi có nhiều kết quả có thể xảy ra.

<p align="center">
  <img src="gif/and_or.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Áp dụng:** Trong bài toán 8 Xe, có thể dùng khi có ràng buộc phụ thuộc giữa các vị trí Xe.

---

### 5.2 Partially Observable Search

**Mô tả:** Áp dụng khi bàn cờ không được quan sát hoàn toàn.

<p align="center">
  <img src="gif/partially_observable.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Áp dụng:** Khi một số vị trí bị ẩn hoặc không thể biết trước, thuật toán phải dự đoán vị trí hợp lệ dựa trên thông tin quan sát được.

---

### 5.3 Belief-State Search

**Mô tả:** Mỗi trạng thái là một tập hợp các khả năng có thể xảy ra.

<p align="center">
  <img src="gif/belief.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Áp dụng:** Hữu ích khi trò chơi có yếu tố không chắc chắn hoặc thiếu thông tin rõ ràng.

---

### Kết luận nhóm Complex Environment

Nhóm này mở rộng mô hình bài toán 8 Xe sang các tình huống không chắc chắn. Tuy chưa phổ biến cho bài toán cơ bản, nhưng hữu ích nếu bài toán mở rộng (ví dụ: Xe ẩn, cấm ô).

---

## 6. Nhóm thuật toán Ràng buộc (CSP - Constraint Satisfaction Problem)

### Tổng quan

Các thuật toán CSP dựa trên ràng buộc giữa các biến và giá trị. Với bài toán 8 Xe, mỗi hàng là một biến, giá trị là cột đặt Xe.

### 6.1 Backtracking

**Mô tả:** Đặt Xe từng bước, nếu xảy ra xung đột thì quay lui.

<p align="center">
  <img src="gif/backtrack.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Ưu điểm:** Đơn giản, hiệu quả với ràng buộc mạnh.  
**Nhược điểm:** Có thể lặp lại nhiều lần, tốn thời gian với không gian lớn.

---

### 6.2 Forward Checking

**Mô tả:** Khi đặt một Xe, loại bỏ các vị trí không hợp lệ của các Xe chưa đặt.

<p align="center">
  <img src="gif/forward.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Ưu điểm:** Giảm đáng kể số lần quay lui.  
**Nhược điểm:** Cần quản lý thêm danh sách miền giá trị hợp lệ.

---

### 6.3 AC-3 (Arc Consistency)

**Mô tả:** Duy trì tính nhất quán trên các cung (Xi, Xj).

<p align="center">
  <img src="gif/ac3.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Ưu điểm:** Giúp rút gọn miền giá trị, giảm thời gian tìm kiếm.  
**Nhược điểm:** Phức tạp hơn về mặt triển khai.

---

### Kết luận nhóm CSP

Các thuật toán CSP là **phù hợp nhất** cho bài toán 8 Xe vì chúng mô hình hóa bài toán bằng ràng buộc “không cùng hàng hoặc cột”. AC-3 và Forward Checking giúp tăng tốc độ đáng kể so với Backtracking truyền thống.

---

## 7. Nhóm thuật toán Đối kháng (Adversarial Search)

### Tổng quan

Nhóm này mô phỏng các trò chơi có hai người chơi đối lập, mỗi bên cố gắng tối ưu chiến lược của mình.

### 7.1 Minimax

**Mô tả:** Mỗi lượt đi được đánh giá dựa trên việc tối thiểu hóa thiệt hại trong trường hợp xấu nhất.

<p align="center">
  <img src="gif/minimax.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Áp dụng:** Giả sử người chơi A đặt Xe, người chơi B thêm chướng ngại; Minimax giúp chọn vị trí đặt Xe tối ưu.  
**Ưu điểm:** Đảm bảo nước đi an toàn nhất.  
**Nhược điểm:** Tốn thời gian nếu không cắt tỉa.

---

### 7.2 Alpha-Beta Pruning

**Mô tả:** Cải tiến Minimax bằng cách loại bỏ các nhánh không cần thiết.

<p align="center">
  <img src="gif/alpha_beta.gif" alt="BFS demo" width="900" style="border-radius:10px;"/>
</p>
**Ưu điểm:** Giảm thời gian tính toán đáng kể.  
**Nhược điểm:** Hiệu quả phụ thuộc vào thứ tự duyệt các trạng thái.

---

### Kết luận nhóm Adversarial Search

Nhóm này phù hợp nếu bài toán được mở rộng thành trò chơi hai người, có yếu tố cạnh tranh hoặc ngẫu nhiên. Alpha-Beta là cải tiến quan trọng giúp Minimax hoạt động hiệu quả hơn.

---

## 8. Tổng kết chung

- **Uninformed Search:** Tìm kiếm toàn diện, chính xác nhưng tốn thời gian và bộ nhớ.
- **Informed Search:** Có định hướng, nhanh hơn và hiệu quả hơn, trong đó A\* nổi bật nhất.
- **Local Search:** Dễ cài đặt, thích hợp cho không gian lớn, nhưng có thể dừng ở nghiệm cục bộ.
- **Complex Environment:** Xử lý môi trường không chắc chắn, phù hợp cho các mở rộng bài toán.
- **CSP:** Phù hợp nhất với bài toán đặt 8 Xe truyền thống nhờ mô hình ràng buộc rõ ràng.
- **Adversarial Search:** Thích hợp cho trò chơi hai người, có yếu tố đối kháng.

Tùy vào mục tiêu (tối ưu, tốc độ, hay mô phỏng thông minh), mỗi nhóm thuật toán có thể được lựa chọn và áp dụng phù hợp cho bài toán đặt quân Xe.
