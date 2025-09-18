import tkinter as tk
from BFS import bfs
from DFS import dfs
from UCS import ucs
from DLS import DLS
from IDS import IDS
from AStar import astar
from GREEDY import greedy
from Luu_duong_di import DuongDi
from chess_ui import Chess


def run_algorithm(algorithm_func):
    """Chạy thuật toán và hiển thị kết quả"""
    result = algorithm_func()

    # Nếu thuật toán trả về (result, visited_states)
    if isinstance(result, tuple) and len(result) == 2:
        final_path, states = result
        storage.cap_nhat_states(states, final_path)

    hien_thi()
    hien_thi_ket_qua_ngay()


def hien_thi():
    """Hiển thị trạng thái trung gian bên trái"""
    state = storage.next_state()
    if state is not None:
        ui.hien_thi_trang_thai_trung_gian(state)
        root.after(100, hien_thi)  # chạy tiếp sau 0.1s


def hien_thi_ket_qua_ngay():
    """Hiển thị kết quả cuối cùng ngay lập tức bên phải"""
    final_state = storage.get_final_state()
    if final_state:
        ui.hien_thi_ket_qua(final_state)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bài toán 8 quân hậu - BFS, DFS, UCS, DLS")
    root.geometry("1200x800")

    # giao diện bàn cờ
    ui = Chess(root)
    storage = DuongDi()

    # danh sách nút bấm
    buttons = [
        ("Bắt đầu BFS", bfs, 2, 0),
        ("Bắt đầu DFS", dfs, 2, 1),
        ("Bắt đầu UCS", ucs, 3, 0),
        ("Bắt đầu DLS", DLS, 3, 1),
        ("Bắt đầu IDDFS", IDS, 4, 0),
        ("Greedy", greedy,4,1),
        ("A*", astar, 5, 0)
    ]

    for text, func, row, col in buttons:
        btn = tk.Button(
            root,
            text=text,
            font=("Arial", 14, "bold"),
            command=lambda f=func: run_algorithm(f)
        )
        btn.grid(row=row, column=col, pady=20)

    root.mainloop()
