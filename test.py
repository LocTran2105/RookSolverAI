import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Custom Combobox Selection")

style = ttk.Style()
style.theme_use("clam")  # 'clam' cho phép chỉnh dễ hơn

style.map("CustomCombobox.TCombobox",
          fieldbackground=[('readonly', '#2e2e2e')],
          selectbackground=[('readonly', '#0078D7')],  # màu khi chọn text
          selectforeground=[('readonly', 'white')],
          background=[('active', '#0078D7')],
          foreground=[('readonly', 'white')],
          arrowcolor=[('active', 'white'), ('!active', 'gray')])

combo = ttk.Combobox(root, values=["BFS", "DFS", "A*", "Greedy"], 
                     style="CustomCombobox.TCombobox", state="readonly")
combo.current(0)
combo.pack(padx=30, pady=30)

root.mainloop()
