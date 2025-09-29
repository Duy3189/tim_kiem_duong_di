import tkinter as tk
from BFS import bfs
from DFS import dfs
from UCS import ucs
from DLS import DLS
from IDS import IDS
from AStar import astar
from Simulated_Annealing import simulated_annealing
from GREEDY import greedy
from Beam_Search import beam_search
from Hill_Climbing import hill_climbing
from genetic_algorithm import genetic_algorithm
from AndOrSearch import and_or_main 
from Belief_state_search import belief_state_main


from Luu_duong_di import DuongDi
from chess_ui import Chess


# --- global ---
is_running = False


def run_algorithm(algorithm_func):
    """Chạy thuật toán và hiển thị kết quả"""
    global is_running
    is_running = False  # reset auto run khi chạy lại

    result = algorithm_func()
    if isinstance(result, tuple) and len(result) == 2:
        final_path, states = result
        storage.cap_nhat_states(states, final_path)

    hien_thi()
    hien_thi_ket_qua_ngay()


def hien_thi():
    """Hiển thị trạng thái tiếp theo"""
    state = storage.next_state()
    if state is not None:
        ui.hien_thi_trang_thai_trung_gian(state)


def hien_thi_ket_qua_ngay():
    """Hiển thị kết quả cuối"""
    final_state = storage.get_final_state()
    if final_state:
        ui.hien_thi_ket_qua(final_state)


def auto_run(delay=500):
    """Chạy tự động"""
    global is_running
    if not is_running:
        return
    state = storage.next_state()
    if state is not None:
        ui.hien_thi_trang_thai_trung_gian(state)
        root.after(delay, auto_run, delay)
    else:
        hien_thi_ket_qua_ngay()
        is_running = False


def start_auto_run():
    global is_running
    is_running = True
    auto_run(500)


def pause_auto_run():
    global is_running
    is_running = False


def show_only(frame, all_frames):
    """Ẩn tất cả frame, chỉ hiện frame được chọn"""
    for f in all_frames:
        f.pack_forget()
    frame.pack(pady=5, fill="x")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bài toán 8 quân hậu - Các thuật toán AI")
    root.geometry("1500x900")

    ui = Chess(root)
    storage = DuongDi()

    frame_buttons = tk.Frame(root)
    frame_buttons.grid(row=0, column=2, rowspan=2, padx=20, pady=20, sticky="n")

    # --- Nhóm 1: Uninformed Search ---
    btn_group1 = tk.Button(frame_buttons, text="Tìm kiếm không có thông tin",
                           font=("Arial", 13, "bold"),
                           width=25, height=2,
                           command=lambda: show_only(frame_group1, [frame_group1, frame_group2, frame_group3]))
    btn_group1.pack(pady=5, fill="x")

    frame_group1 = tk.Frame(frame_buttons)
    uninformed = [
        ("BFS", bfs),
        ("DFS", dfs),
        ("DLS", DLS),
        ("IDS", IDS),
    ]
    for text, func in uninformed:
        tk.Button(frame_group1, text=text, font=("Arial", 12),
                  width=20, height=2,
                  command=lambda f=func: run_algorithm(f)).pack(pady=3)

    # --- Nhóm 2: Informed Search ---
    btn_group2 = tk.Button(frame_buttons, text="Tìm kiếm có thông tin",
                           font=("Arial", 13, "bold"),
                           width=25, height=2,
                           command=lambda: show_only(frame_group2, [frame_group1, frame_group2, frame_group3]))
    btn_group2.pack(pady=5, fill="x")

    frame_group2 = tk.Frame(frame_buttons)
    informed = [
        ("UCS", ucs),
        ("A*", astar),
        ("Greedy", greedy),
    ]
    for text, func in informed:
        tk.Button(frame_group2, text=text, font=("Arial", 12),
                  width=20, height=2,
                  command=lambda f=func: run_algorithm(f)).pack(pady=3)

    # --- Nhóm 3: Local Search ---
    btn_group3 = tk.Button(frame_buttons, text="Local Search",
                           font=("Arial", 13, "bold"),
                           width=25, height=2,
                           command=lambda: show_only(frame_group3, [frame_group1, frame_group2, frame_group3]))
    btn_group3.pack(pady=5, fill="x")

    frame_group3 = tk.Frame(frame_buttons)
    local_search = [
        ("Hill Climbing", hill_climbing),
        ("Simulated Annealing", simulated_annealing),
        ("Beam Search", beam_search),
        ("Genetic Algorithm", genetic_algorithm),
    ]
    for text, func in local_search:
        tk.Button(frame_group3, text=text, font=("Arial", 12),
                  width=20, height=2,
                  command=lambda f=func: run_algorithm(f)).pack(pady=3)
    
    # --- Nhóm 4: Môi trường không xác định ---
    btn_group4 = tk.Button(frame_buttons, text="Môi trường không xác định",
                           font=("Arial", 13, "bold"),
                           width=25, height=2,
                           command=lambda: show_only(frame_group4, [frame_group1, frame_group2, frame_group3, frame_group4]))
    btn_group4.pack(pady=5, fill="x")

    frame_group4 = tk.Frame(frame_buttons)
    uncertain_env = [
        ("And-Or Search", and_or_main),
        ("Belief state search", belief_state_main),
    ]
    for text, func in uncertain_env:
        tk.Button(frame_group4, text=text, font=("Arial", 12),
                  width=20, height=2,
                  command=lambda f=func: run_algorithm(f)).pack(pady=3)

    # --- Điều khiển ---
    label_ctrl = tk.Label(frame_buttons, text="Điều khiển", font=("Arial", 12, "bold"))
    label_ctrl.pack(pady=(20, 5))

    btn_next = tk.Button(frame_buttons, text="Next Step", font=("Arial", 12, "bold"),
                         width=20, height=2, command=hien_thi)
    btn_next.pack(pady=5)

    btn_auto = tk.Button(frame_buttons, text="Auto Run", font=("Arial", 12, "bold"),
                         width=20, height=2, command=start_auto_run)
    btn_auto.pack(pady=5)

    btn_pause = tk.Button(frame_buttons, text="Pause", font=("Arial", 12, "bold"),
                          width=20, height=2, command=pause_auto_run)
    btn_pause.pack(pady=5)

    root.mainloop()
