# 8 Rooks Solver AI

Project giải bài toán 8 quân xe (8 Rooks Problem) sử dụng các thuật toán AI.

## Bài toán

Đặt 8 quân xe trên bàn cờ 8x8 sao cho không quân nào có thể ăn được quân nào khác.
Quân xe có thể di chuyển theo hàng ngang và hàng dọc.

## Cài đặt

Project sử dụng Python 3 với thư viện tkinter (có sẵn trong Python).

## Tính năng

- Giao diện trực quan với bàn cờ 8x8 responsive
- 5 nhóm thuật toán AI:
  - **Uninformed Search**: BFS, DFS, UCS, IDS
  - **Informed Search**: Greedy, A*, IDA*
  - **Local Search**: Hill Climbing, Simulated Annealing, Genetic Algorithm
  - **Complex Environment**: Minimax, Alpha-Beta Pruning
  - **CSP**: Backtracking, Forward Checking, AC-3
- Hiển thị quá trình giải theo thời gian thực
- Thống kê chi tiết: thuật toán, thời gian, số bước
- Bàn cờ tự động scale khi resize window

## Cách sử dụng

1. Chọn thuật toán từ panel bên phải (hiện tại chỉ BFS khả dụng)
2. Nhấn nút **START** để bắt đầu giải bài toán
3. Quan sát quá trình đặt quân xe trên bàn cờ
4. Xem thống kê trong phần Statistics
5. Nhấn **RESET** để làm mới bàn cờ

## Mở rộng

Để thêm thuật toán mới:

1. Tạo file mới trong thư mục `algo/` (ví dụ: `dfs.py`)
2. Implement class solver với method `solve(callback)` trả về `(solution, steps, time_taken)`
3. Cập nhật `main.py` để import và sử dụng thuật toán mới

## Ghi chú

- Hiện tại chỉ thuật toán BFS được implement
- Các thuật toán khác sẽ được thêm vào sau
- Gửi code thuật toán của bạn để tích hợp vào project
