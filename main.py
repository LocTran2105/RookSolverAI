import tkinter as tk
from tkinter import ttk, messagebox
import threading

from algo.dfs import DFSSolver
from algo.bfs import BFSSolver
from algo.astar import AStarSolver
from algo.greedy import GreedySolver
from algo.ids import IDSSolver
from algo.ucs import UCSSolver
from algo.genetic import GeneticSolver
from algo.hill_climbing import HillClimbingSolver
from algo.dls import DLSSolver
from algo.beam_search import BeamSearchSolver
from algo.simulated_annealing import SimulatedAnnealingSolver
from algo.or_and_tree import ORAndTreeSolver
from algo.backtracking import BacktrackingSolver
from algo.forward_checking import ForwardCheckingSolver
from algo.ac3 import AC3Solver
from algo.belief_state import BeliefStateSolver
from algo.minimax import Minimax
from algo.alpha_beta import AlphaBetaSolver
from algo.partially_observable import PartiallyObservableSolver

class RooksSolverUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Rooks Solver - AI Algorithms")
        self.root.geometry("1500x900")
        self.root.configure(bg="#1a1a2e")
        self.root.minsize(1400, 850)
        
        self.n = 8
        self.cell_size = 70
        
        self.bfs_solver = BFSSolver(self.n)
        self.dfs_solver = DFSSolver(self.n)
        self.astar_solver = AStarSolver(self.n)
        self.greedy_solver = GreedySolver(self.n)
        self.ids_solver = IDSSolver(self.n)
        self.ucs_solver = UCSSolver(self.n)
        self.genetic_solver = GeneticSolver(self.n)
        self.hill_climbing_solver = HillClimbingSolver(self.n)
        self.dls_solver = DLSSolver(self.n)
        self.beam_solver = BeamSearchSolver(self.n)
        self.sa_solver = SimulatedAnnealingSolver(self.n)
        self.or_and_solver = ORAndTreeSolver(self.n)
        self.backtracking_solver = BacktrackingSolver(self.n)
        self.forward_checking_solver = ForwardCheckingSolver(self.n)
        self.ac3_solver = AC3Solver(self.n)
        self.belief_state_solver = BeliefStateSolver(self.n)
        self.adversarial_solver = Minimax(self.n)
        self.alpha_beta_solver = AlphaBetaSolver(self.n)
        self.partially_observable_solver = PartiallyObservableSolver(self.n)
        
        self.current_solver = self.bfs_solver
        self.current_algorithm = "BFS"
        self.is_solving = False
        self.solving_thread = None
        self.current_solution = []
        self.current_cost = 0
        self.current_nodes = 0
        
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0
        
        self.first_position = None
        
        self.setup_ui()
        
        self.root.bind('<Configure>', self.on_window_resize)

    def on_window_resize(self, event):
        """Xử lý khi resize window để giữ bàn cờ cân xứng"""
        if event.widget == self.root:
            available_height = self.root.winfo_height() - 150
            available_width = (self.root.winfo_width() - 500) 
            new_size = min(available_height, available_width) // self.n
            
            if new_size > 40 and new_size != self.cell_size:
                self.cell_size = new_size
                self.canvas.config(
                    width=self.cell_size * self.n,
                    height=self.cell_size * self.n
                )
                self.draw_board(self.current_solution if self.current_solution else None)
        
    def setup_ui(self):
        """Thiết lập giao diện"""
        main_container = tk.Frame(self.root, bg="#1a1a2e")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Bên trái: Bàn cờ
        left_frame = tk.Frame(main_container, bg="#1a1a2e")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # Title
        title = tk.Label(
            left_frame,
            text="8 ROOKS PROBLEM",
            font=("Arial", 22, "bold"),
            bg="#1a1a2e",
            fg="#00d4ff"
        )
        title.pack(pady=(0, 10))
        
        canvas_container = tk.Frame(left_frame, bg="#1a1a2e")
        canvas_container.pack(expand=True)
        
        # Canvas cho bàn cờ
        self.canvas = tk.Canvas(
            canvas_container,
            width=self.cell_size * self.n,
            height=self.cell_size * self.n,
            bg="#16213e",
            highlightthickness=2,
            highlightbackground="#00d4ff"
        )
        self.canvas.pack()
        
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        self.draw_board()
        
        # Bên phải: Control Panel với ScrollBar
        right_frame = tk.Frame(main_container, bg="#16213e", width=500)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        right_frame.pack_propagate(False)
        
        # Title panel
        panel_title = tk.Label(
            right_frame,
            text="CONTROL PANEL",
            font=("Arial", 14, "bold"),
            bg="#16213e",
            fg="#00d4ff"
        )
        panel_title.pack(pady=(10, 5))
        
        # Tạo canvas và scrollbar cho phần algorithms
        canvas_frame = tk.Frame(right_frame, bg="#16213e")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        algo_canvas = tk.Canvas(canvas_frame, bg="#16213e", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=algo_canvas.yview)
        scrollable_frame = tk.Frame(algo_canvas, bg="#16213e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: algo_canvas.configure(scrollregion=algo_canvas.bbox("all"))
        )
        
        algo_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        algo_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Đặt các nhóm thuật toán vào scrollable frame
        self.create_algorithm_group(
            scrollable_frame,
            "UNINFORMED SEARCH",
            ["BFS", "DFS", "UCS", "IDS", "DLS"]
        )
        
        self.create_algorithm_group(
            scrollable_frame,
            "INFORMED SEARCH",
            ["Greedy", "A*"]
        )
        
        self.create_algorithm_group(
            scrollable_frame,
            "LOCAL SEARCH",
            ["Hill Climbing", "Genetic", "Beam", "SA"]
        )
        
        self.create_algorithm_group(
            scrollable_frame,
            "CSP",
            ["Backtracking", "Forward Check", "AC3"]
        )
        
        self.create_algorithm_group(
            scrollable_frame,
            "COMPLEX ENVIRONMENT",
            ["Belief State", "OR-AND", "Partially Observable"]
        )
        
        self.create_algorithm_group(
            scrollable_frame,
            "ADVERSARIAL",
            ["Minimax", "Alpha-Beta"]
        )
        
        algo_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            algo_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        algo_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Separator
        separator = tk.Frame(right_frame, height=2, bg="#00d4ff")
        separator.pack(fill=tk.X, pady=5, padx=15)
        
        # Buttons
        button_frame = tk.Frame(right_frame, bg="#16213e")
        button_frame.pack(pady=5, padx=15, fill=tk.X)
        
        self.start_btn = tk.Button(
            button_frame,
            text="▶ START",
            font=("Arial", 11, "bold"),
            bg="#4ecca3",
            fg="#1a1a2e",
            activebackground="#3daa82",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.start_solving
        )
        self.start_btn.pack(side=tk.LEFT, pady=5, padx=5, fill=tk.BOTH, expand=True, ipady=8)
        
        self.reset_btn = tk.Button(
            button_frame,
            text="↻ RESET",
            font=("Arial", 11, "bold"),
            bg="#ff6b6b",
            fg="#ffffff",
            activebackground="#cc5555",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.reset_board
        )
        self.reset_btn.pack(side=tk.LEFT, pady=5, padx=5, fill=tk.BOTH, expand=True, ipady=8)
        
        # Statistics frame - cố định ở dưới
        stats_frame = tk.Frame(right_frame, bg="#1a1a2e", relief=tk.RIDGE, bd=2)
        stats_frame.pack(pady=5, padx=15, fill=tk.X, side=tk.BOTTOM)
        
        stats_frame.grid_columnconfigure(0, weight=1, minsize=150)
        stats_frame.grid_columnconfigure(1, weight=1, minsize=150)
        stats_frame.grid_columnconfigure(2, weight=1, minsize=150)
        
        stats_title = tk.Label(
            stats_frame,
            text="STATISTICS",
            font=("Arial", 11, "bold"),
            bg="#1a1a2e",
            fg="#00d4ff"
        )
        stats_title.grid(row=0, column=0, columnspan=3, pady=(5, 5), sticky="ew")
        
        # Algorithm (full width)
        self.algo_label = tk.Label(
            stats_frame,
            text="Algorithm: BFS",
            font=("Arial", 9, "bold"),
            bg="#1a1a2e",
            fg="#ffd93d",
            anchor="w",
            width=40
        )
        self.algo_label.grid(row=1, column=0, columnspan=3, pady=3, padx=10, sticky="w")
        
        # Row 2: Time and Steps
        self.time_label = tk.Label(
            stats_frame,
            text="Time: 0.000s",
            font=("Arial", 9),
            bg="#1a1a2e",
            fg="#ffffff",
            anchor="w",
            width=18
        )
        self.time_label.grid(row=2, column=0, columnspan=2, pady=2, padx=10, sticky="w")
        
        self.steps_label = tk.Label(
            stats_frame,
            text="Steps: 0",
            font=("Arial", 9),
            bg="#1a1a2e",
            fg="#ffffff",
            anchor="e",
            width=12
        )
        self.steps_label.grid(row=2, column=2, pady=2, padx=10, sticky="e")
        
        # Row 3: Nodes and Cost
        self.nodes_label = tk.Label(
            stats_frame,
            text="Nodes: 0",
            font=("Arial", 9),
            bg="#1a1a2e",
            fg="#ffffff",
            anchor="w",
            width=18
        )
        self.nodes_label.grid(row=3, column=0, columnspan=2, pady=2, padx=10, sticky="w")
        
        self.cost_label = tk.Label(
            stats_frame,
            text="Cost: 0.00",
            font=("Arial", 9),
            bg="#1a1a2e",
            fg="#ffffff",
            anchor="e",
            width=12
        )
        self.cost_label.grid(row=3, column=2, pady=2, padx=10, sticky="e")
        
        cost_separator = tk.Frame(stats_frame, height=1, bg="#00d4ff")
        cost_separator.grid(row=4, column=0, columnspan=3, pady=(5, 3), padx=10, sticky="ew")
        
        cost_title = tk.Label(
            stats_frame,
            text="COST METRICS",
            font=("Arial", 9, "bold"),
            bg="#1a1a2e",
            fg="#00d4ff"
        )
        cost_title.grid(row=5, column=0, columnspan=3, pady=(0, 3), sticky="ew")
        
        # Row 6: g(x), h(x), f(x)
        self.g_cost_label = tk.Label(
            stats_frame,
            text="g(x): 0",
            font=("Arial", 10, "bold"),
            bg="#2d3e50",
            fg="#4ecca3",
            anchor="center",
            width=12,
            relief=tk.FLAT,
            padx=5,
            pady=4
        )
        self.g_cost_label.grid(row=6, column=0, pady=3, padx=5, sticky="ew")
        
        self.h_cost_label = tk.Label(
            stats_frame,
            text="h(x): 0",
            font=("Arial", 10, "bold"),
            bg="#2d3e50",
            fg="#ffd93d",
            anchor="center",
            width=12,
            relief=tk.FLAT,
            padx=5,
            pady=4
        )
        self.h_cost_label.grid(row=6, column=1, pady=3, padx=5, sticky="ew")
        
        self.f_cost_label = tk.Label(
            stats_frame,
            text="f(x): 0",
            font=("Arial", 10, "bold"),
            bg="#2d3e50",
            fg="#ff6b6b",
            anchor="center",
            width=12,
            relief=tk.FLAT,
            padx=5,
            pady=4
        )
        self.f_cost_label.grid(row=6, column=2, pady=3, padx=5, sticky="ew")
        
        # Status
        self.status_label = tk.Label(
            stats_frame,
            text="Status: Click để đặt quân đầu tiên",
            font=("Arial", 9, "bold"),
            bg="#1a1a2e",
            fg="#4ecca3",
            anchor="w",
            wraplength=450,
            width=40
        )
        self.status_label.grid(row=7, column=0, columnspan=3, pady=(5, 8), padx=10, sticky="w")
    
    def create_algorithm_group(self, parent, title, algorithms):
        """Tạo nhóm thuật toán với các nút nằm ngang"""
        group_frame = tk.Frame(parent, bg="#16213e")
        group_frame.pack(pady=5, padx=10, fill=tk.X)
        
        group_title = tk.Label(
            group_frame,
            text=title,
            font=("Arial", 9, "bold"),
            bg="#16213e",
            fg="#00d4ff"
        )
        group_title.pack(anchor="w", pady=(0, 3))
        
        buttons_frame = tk.Frame(group_frame, bg="#16213e")
        buttons_frame.pack(fill=tk.X)
        
        for algo in algorithms:
            state = tk.NORMAL
            bg_color = "#00d4ff" if algo == "BFS" else "#2d3e50"
            fg_color = "#1a1a2e" if algo == "BFS" else "#ffffff"
            
            btn = tk.Button(
                buttons_frame,
                text=algo,
                font=("Arial", 8, "bold"),
                bg=bg_color,
                fg=fg_color,
                activebackground="#00a8cc",
                activeforeground="#ffffff",
                relief=tk.FLAT,
                cursor="hand2",
                state=state,
                padx=8,
                pady=4,
                command=lambda a=algo: self.select_algorithm(a)
            )
            btn.pack(side=tk.LEFT, padx=3, pady=2)
            
            if not hasattr(self, 'algo_buttons'):
                self.algo_buttons = {}
            self.algo_buttons[algo] = btn
    
    def select_algorithm(self, algo_name):
        """Chọn thuật toán"""
        for algo, btn in self.algo_buttons.items():
            if btn['state'] == tk.NORMAL:
                if algo == algo_name:
                    btn.config(bg="#00d4ff", fg="#1a1a2e")
                else:
                    btn.config(bg="#2d3e50", fg="#ffffff")
        
        self.current_algorithm = algo_name
        self.algo_label.config(text=f"Algorithm: {algo_name}")
        
        solver_map = {
            "BFS": self.bfs_solver,
            "DFS": self.dfs_solver,
            "A*": self.astar_solver,
            "Greedy": self.greedy_solver,
            "IDS": self.ids_solver,
            "UCS": self.ucs_solver,
            "Genetic": self.genetic_solver,
            "Hill Climbing": self.hill_climbing_solver,
            "DLS": self.dls_solver,
            "Beam": self.beam_solver,
            "SA": self.sa_solver,
            "OR-AND": self.or_and_solver,
            "Backtracking": self.backtracking_solver,
            "Forward Check": self.forward_checking_solver,
            "AC3": self.ac3_solver,
            "Belief State": self.belief_state_solver,
            "Minimax": self.adversarial_solver,
            "Alpha-Beta": self.alpha_beta_solver,
            "Partially Observable": self.partially_observable_solver
        }
        
        self.current_solver = solver_map.get(algo_name, self.bfs_solver)
    
    def on_canvas_click(self, event):
        if self.is_solving or self.current_solution:
            return
        
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if 0 <= row < self.n and 0 <= col < self.n:
            self.first_position = (row, col)
            self.draw_board()
            self.status_label.config(
                text=f"Trạng thái: Quân đầu tiên đã đặt tại hàng {row}, cột {col}. Bấm START để giải",
                fg="#ffd93d"
            )
    
    def draw_board(self, solution=None):
        """Vẽ bàn cờ"""
        self.canvas.delete("all")
        
        for row in range(self.n):
            for col in range(self.n):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                color = "#e8e8e8" if (row + col) % 2 == 0 else "#0f3460"
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="#00d4ff",
                    width=1
                )
        
        if self.first_position and not solution:
            row, col = self.first_position
            x = col * self.cell_size + self.cell_size // 2
            y = row * self.cell_size + self.cell_size // 2
            
            font_size = int(self.cell_size * 0.6)
            self.canvas.create_text(
                x, y,
                text="♜",
                font=("Arial", font_size),
                fill="#4ecca3"
            )
        
        if solution:
            for row in range(len(solution)):
                col = solution[row]
                # Only draw if the rook has been placed (col != -1)
                if col != -1:
                    x = col * self.cell_size + self.cell_size // 2
                    y = row * self.cell_size + self.cell_size // 2
                    
                    font_size = int(self.cell_size * 0.6)
                    self.canvas.create_text(
                        x, y,
                        text="♜",
                        font=("Arial", font_size),
                        fill="#ff6b6b"
                    )
    
    def update_callback(self, board, steps):
        """Callback để cập nhật UI trong quá trình giải"""
        self.root.after(0, lambda: self.draw_board(board))
        self.root.after(0, lambda: self.steps_label.config(text=f"Steps: {steps}"))
        self.root.after(0, lambda: self.nodes_label.config(text=f"Nodes: {steps}"))
        threading.Event().wait(0.001)
    
    def start_solving(self):
        """Bắt đầu giải bài toán"""
        if self.is_solving:
            return
        
        if not self.first_position:
            self.status_label.config(
                text="Trạng thái: Vui lòng đặt quân đầu tiên trước!",
                fg="#ff6b6b"
            )
            return
        
        self.is_solving = True
        self.start_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Solving...", fg="#ffd93d")
        
        def solve_thread():
            result = self.current_solver.solve(self.update_callback, self.first_position)
            
            # Handle different return formats from different algorithms
            try:
                if len(result) == 6:
                    # A* algorithm returns 6 values
                    solution, nodes, time_taken, g_cost, h_cost, f_cost = result
                    self.g_cost = g_cost
                    self.h_cost = h_cost
                    self.f_cost = f_cost
                    self.current_cost = f_cost
                elif len(result) == 4:
                    # Greedy, UCS, Beam, SA return 4 values
                    solution, nodes, time_taken, extra_cost = result
                    if self.current_algorithm == "Greedy":
                        self.h_cost = extra_cost
                        self.g_cost = 0
                        self.f_cost = 0
                        self.current_cost = extra_cost
                    elif self.current_algorithm == "UCS":
                        self.g_cost = extra_cost
                        self.h_cost = 0
                        self.f_cost = 0
                        self.current_cost = extra_cost
                    else:  # Beam, SA, or others
                        self.current_cost = extra_cost
                        self.g_cost = 0
                        self.h_cost = 0
                        self.f_cost = 0
                elif len(result) == 3:
                    # BFS, DFS, IDS, DLS and other algorithms return 3 values
                    solution, nodes, time_taken = result
                    self.current_cost = 0
                    self.g_cost = 0
                    self.h_cost = 0
                    self.f_cost = 0
                else:
                    # Fallback for unexpected return format
                    print(f"[v0] Unexpected result length: {len(result)}")
                    solution = result[0] if len(result) > 0 else []
                    nodes = result[1] if len(result) > 1 else 0
                    time_taken = result[2] if len(result) > 2 else 0
                    self.current_cost = 0
                    self.g_cost = 0
                    self.h_cost = 0
                    self.f_cost = 0
            except Exception as e:
                print(f"[v0] Error unpacking result: {e}")
                # Safe fallback
                solution = []
                nodes = 0
                time_taken = 0
                self.current_cost = 0
                self.g_cost = 0
                self.h_cost = 0
                self.f_cost = 0
            
            self.current_nodes = nodes
            
            self.root.after(0, lambda: self.finish_solving(solution, nodes, time_taken))
        
        self.solving_thread = threading.Thread(target=solve_thread, daemon=True)
        self.solving_thread.start()

    def finish_solving(self, solution, steps, time_taken):
        """Hoàn thành việc giải"""
        self.is_solving = False
        self.current_solution = solution
        
        if solution and len(solution) == 8:
            self.draw_board(solution)
            self.status_label.config(text="Status: Solved ✓", fg="#4ecca3")
            self.time_label.config(text=f"Time: {time_taken:.3f}s")
            self.steps_label.config(text=f"Steps: {steps}")
            self.nodes_label.config(text=f"Nodes: {steps}")
            
            if isinstance(self.current_cost, float):
                self.cost_label.config(text=f"Cost: {self.current_cost:.2f}")
            else:
                self.cost_label.config(text=f"Cost: {self.current_cost}")
            
            if isinstance(self.g_cost, float):
                self.g_cost_label.config(text=f"g(x): {self.g_cost:.2f}")
            else:
                self.g_cost_label.config(text=f"g(x): {self.g_cost}")
                
            if isinstance(self.h_cost, float):
                self.h_cost_label.config(text=f"h(x): {self.h_cost:.2f}")
            else:
                self.h_cost_label.config(text=f"h(x): {self.h_cost}")
                
            if isinstance(self.f_cost, float):
                self.f_cost_label.config(text=f"f(x): {self.f_cost:.2f}")
            else:
                self.f_cost_label.config(text=f"f(x): {self.f_cost}")
        else:
            self.draw_board()
            self.status_label.config(text="Status: No solution found", fg="#ff6b6b")
            
            rooks_placed = len(solution) if solution else 0
            messagebox.showwarning(
                "Không tìm thấy lời giải",
                f"Không thể đặt đủ 8 quân cờ cho vị trí đã chọn!\n\n"
                f"Vị trí đã đặt: Hàng {self.first_position[0]}, Cột {self.first_position[1]}\n"
                f"Thuật toán: {self.current_algorithm}\n"
                f"Số quân đã đặt được: {rooks_placed}/8\n"
                f"Số bước đã thử: {steps}\n"
                f"Thời gian: {time_taken:.3f}s\n\n"
                f"Hãy thử đặt quân cờ ở vị trí khác!"
            )
            
            self.time_label.config(text=f"Time: {time_taken:.3f}s")
            self.steps_label.config(text=f"Steps: {steps}")
            self.nodes_label.config(text=f"Nodes: {steps}")
            self.cost_label.config(text=f"Cost: 0.00")
            self.g_cost_label.config(text=f"g(x): 0")
            self.h_cost_label.config(text=f"h(x): 0")
            self.f_cost_label.config(text=f"f(x): 0")
        
        self.start_btn.config(state=tk.NORMAL)
    
    def reset_board(self):
        """Reset bàn cờ và dừng thuật toán hiện tại"""
        self.is_solving = False
        
        self.first_position = None
        
        self.current_solution = []
        self.current_cost = 0
        self.current_nodes = 0
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0
        
        self.draw_board()
        
        self.time_label.config(text="Time: 0.000s")
        self.steps_label.config(text="Steps: 0")
        self.nodes_label.config(text="Nodes: 0")
        self.cost_label.config(text="Cost: 0.00")
        self.g_cost_label.config(text="g(x): 0")
        self.h_cost_label.config(text="h(x): 0")
        self.f_cost_label.config(text="f(x): 0")
        self.status_label.config(text="Trạng thái: Click để đặt quân đầu tiên", fg="#4ecca3")
        self.start_btn.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = RooksSolverUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
