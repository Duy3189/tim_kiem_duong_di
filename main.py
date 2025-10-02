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
from part_infor import partial_goal_main_bfs
from part_info_ui import open_part_info_ui
from CSP import backtracking_main, forward_checking_main, compare_csp_algorithms  # THÊM DÒNG NÀY

from Luu_duong_di import DuongDi
from chess_ui import Chess

# --- global ---
is_running = False
storage = None
ui = None

def run_algorithm(algorithm_func, *args):
    """Chạy thuật toán và hiển thị kết quả"""
    global is_running, storage
    is_running = False  # reset auto run khi chạy lại

    try:
        result = algorithm_func(*args)
        if isinstance(result, tuple) and len(result) == 2:
            final_path, states = result
            storage.cap_nhat_states(states, final_path)
        else:
            print(f"Kết quả không hợp lệ từ {algorithm_func.__name__}")

        hien_thi()
        hien_thi_ket_qua_ngay()
    except Exception as e:
        print(f"Lỗi khi chạy thuật toán: {e}")

def run_part_info_search():
    """Chạy Part Information Search với giao diện nhập liệu"""
    def on_partial_goal_received(partial_goal):
        """Callback khi nhận được partial goal từ UI"""
        if partial_goal:
            print(f"✅ Đã nhận partial goal: {partial_goal}")
            print("🔄 Đang bắt đầu tìm kiếm...")
            run_algorithm(partial_goal_main_bfs, 8, partial_goal)
    
    print("📝 Mở giao diện nhập Part Information...")
    open_part_info_ui(root, on_partial_goal_received)

def hien_thi():
    """Hiển thị trạng thái tiếp theo"""
    if storage:
        state = storage.next_state()
        if state is not None and ui:
            ui.hien_thi_trang_thai_trung_gian(state)

def hien_thi_ket_qua_ngay():
    """Hiển thị kết quả cuối"""
    if storage:
        final_state = storage.get_final_state()
        if final_state and ui:
            ui.hien_thi_ket_qua(final_state)

def auto_run(delay=500):
    """Chạy tự động"""
    global is_running
    if not is_running or not storage:
        return
    state = storage.next_state()
    if state is not None and ui:
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

def create_button(parent, text, command, font=("Arial", 12), width=20, height=2):
    """Tạo button an toàn"""
    try:
        return tk.Button(parent, text=text, font=font, width=width, height=height, command=command)
    except tk.TclError:
        return None

if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.title("Bài toán 8 quân hậu - Các thuật toán AI")
        root.geometry("1500x900")

        ui = Chess(root)
        storage = DuongDi()

        frame_buttons = tk.Frame(root)
        frame_buttons.grid(row=0, column=2, rowspan=2, padx=20, pady=20, sticky="n")

        # --- Nhóm 1: Uninformed Search ---
        btn_group1 = create_button(frame_buttons, "Tìm kiếm không có thông tin", 
                                 font=("Arial", 13, "bold"), width=25, height=2,
                                 command=lambda: show_only(frame_group1, [frame_group1, frame_group2, frame_group3, frame_group4, frame_group5]))
        if btn_group1:
            btn_group1.pack(pady=5, fill="x")

        frame_group1 = tk.Frame(frame_buttons)
        uninformed = [
            ("BFS", bfs),
            ("DFS", dfs),
            ("DLS", DLS),
            ("IDS", IDS),
        ]
        for text, func in uninformed:
            btn = create_button(frame_group1, text, lambda f=func: run_algorithm(f))
            if btn:
                btn.pack(pady=3)

        # --- Nhóm 2: Informed Search ---
        btn_group2 = create_button(frame_buttons, "Tìm kiếm có thông tin",
                                 font=("Arial", 13, "bold"), width=25, height=2,
                                 command=lambda: show_only(frame_group2, [frame_group1, frame_group2, frame_group3, frame_group4, frame_group5]))
        if btn_group2:
            btn_group2.pack(pady=5, fill="x")

        frame_group2 = tk.Frame(frame_buttons)
        informed = [
            ("UCS", ucs),
            ("A*", astar),
            ("Greedy", greedy),
        ]
        for text, func in informed:
            btn = create_button(frame_group2, text, lambda f=func: run_algorithm(f))
            if btn:
                btn.pack(pady=3)

        # --- Nhóm 3: Local Search ---
        btn_group3 = create_button(frame_buttons, "Local Search",
                                 font=("Arial", 13, "bold"), width=25, height=2,
                                 command=lambda: show_only(frame_group3, [frame_group1, frame_group2, frame_group3, frame_group4, frame_group5]))
        if btn_group3:
            btn_group3.pack(pady=5, fill="x")

        frame_group3 = tk.Frame(frame_buttons)
        local_search = [
            ("Hill Climbing", hill_climbing),
            ("Simulated Annealing", simulated_annealing),
            ("Beam Search", beam_search),
            ("Genetic Algorithm", genetic_algorithm),
        ]
        for text, func in local_search:
            btn = create_button(frame_group3, text, lambda f=func: run_algorithm(f))
            if btn:
                btn.pack(pady=3)
        
        # --- Nhóm 4: Môi trường không xác định ---
        btn_group4 = create_button(frame_buttons, "Môi trường không xác định",
                                 font=("Arial", 13, "bold"), width=25, height=2,
                                 command=lambda: show_only(frame_group4, [frame_group1, frame_group2, frame_group3, frame_group4, frame_group5]))
        if btn_group4:
            btn_group4.pack(pady=5, fill="x")

        frame_group4 = tk.Frame(frame_buttons)
        uncertain_env = [
            ("And-Or Search", and_or_main),
            ("Belief state search", lambda: run_algorithm(belief_state_main)),
            ("Part information", run_part_info_search)
        ]
        for text, func in uncertain_env:
            btn = create_button(frame_group4, text, func)
            if btn:
                btn.pack(pady=3)

        # --- NHÓM 5: CSP ALGORITHMS ---
        btn_group5 = create_button(frame_buttons, "CSP Algorithms",
                                 font=("Arial", 13, "bold"), width=25, height=2,
                                 command=lambda: show_only(frame_group5, [frame_group1, frame_group2, frame_group3, frame_group4, frame_group5]))
        if btn_group5:
            btn_group5.pack(pady=5, fill="x")

        frame_group5 = tk.Frame(frame_buttons)
        csp_algorithms = [
            ("Backtracking", lambda: run_algorithm(backtracking_main)),
            ("Forward Checking", lambda: run_algorithm(forward_checking_main)),
            ("Compare CSP", lambda: compare_csp_algorithms(8))
        ]
        for text, func in csp_algorithms:
            btn = create_button(frame_group5, text, func)
            if btn:
                btn.pack(pady=3)

        # --- Điều khiển ---
        label_ctrl = tk.Label(frame_buttons, text="Điều khiển", font=("Arial", 12, "bold"))
        label_ctrl.pack(pady=(20, 5))

        btn_next = create_button(frame_buttons, "Next Step", hien_thi, font=("Arial", 12, "bold"))
        if btn_next:
            btn_next.pack(pady=5)

        btn_auto = create_button(frame_buttons, "Auto Run", start_auto_run, font=("Arial", 12, "bold"))
        if btn_auto:
            btn_auto.pack(pady=5)

        btn_pause = create_button(frame_buttons, "Pause", pause_auto_run, font=("Arial", 12, "bold"))
        if btn_pause:
            btn_pause.pack(pady=5)

        # Hiển thị nhóm đầu tiên
        show_only(frame_group1, [frame_group1, frame_group2, frame_group3, frame_group4, frame_group5])

        root.mainloop()
        
    except Exception as e:
        print(f"Lỗi khởi chạy ứng dụng: {e}")