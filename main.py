import tkinter as tk
from BFS import bfs
from DFS import dfs
from UCS import ucs
from Luu_duong_di import DuongDi
from chess_ui import Chess
  

def chay_bfs():
    states = bfs()
    if states:
        storage.cap_nhat_states(states)
        hien_thi()                 # diễn tiến bên trái
        hien_thi_ket_qua_ngay()     # kết quả cuối bên phải

def chay_dfs():
    states = dfs()
    if states:
        storage.cap_nhat_states(states)
        hien_thi()
        hien_thi_ket_qua_ngay()

def chay_ucs():
    states = ucs()
    if states:
        storage.cap_nhat_states(states)
        hien_thi()
        hien_thi_ket_qua_ngay()


def hien_thi():
    """Hiển thị trạng thái trung gian bên trái"""
    state = storage.next_state()
    if state is not None:
        ui.hien_thi_trang_thai_trung_gian(state)
        root.after(300, hien_thi)   # chạy tiếp sau 0.3s


def hien_thi_ket_qua_ngay():
    """Hiển thị kết quả cuối cùng ngay lập tức bên phải"""
    final_state = storage.get_final_state()
    if final_state:
        ui.hien_thi_ket_qua(final_state)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bài toán 8 quân hậu - BFS, DFS, UCS")
    root.geometry("1200x800")

    # giao diện bàn cờ
    ui = Chess(root)
    storage = DuongDi()

    # nút bấm BFS
    start_bfs_btn = tk.Button(root, text="Bắt đầu BFS", font=("Arial", 14, "bold"),
                              command=chay_bfs)
    start_bfs_btn.grid(row=2, column=0, pady=20)

    # nút bấm DFS
    start_dfs_btn = tk.Button(root, text="Bắt đầu DFS", font=("Arial", 14, "bold"),
                              command=chay_dfs)
    start_dfs_btn.grid(row=2, column=1, pady=20)

    # nút bấm UCS
    start_ucs_btn = tk.Button(root, text="Bắt đầu UCS", font=("Arial", 14, "bold"),
                              command=chay_ucs)
    start_ucs_btn.grid(row=3, column=0, columnspan=2, pady=20)

    root.mainloop()
