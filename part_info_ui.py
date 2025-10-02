import tkinter as tk
from tkinter import messagebox

class PartInfoUI:
    def __init__(self, parent, n=8):
        self.parent = parent
        self.n = n
        self.partial_goal = {}
        self.result_callback = None
        self.create_widgets()
    
    def create_widgets(self):
        """Tạo giao diện nhập partial goal"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Nhập thông tin một phần")
        self.window.geometry("450x500")
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Tiêu đề
        title_label = tk.Label(self.window, 
                              text="NHẬP THÔNG TIN ĐÃ BIẾT", 
                              font=("Arial", 16, "bold"),
                              fg="#2E86AB")
        title_label.pack(pady=15)
        
        # Giải thích
        explain_label = tk.Label(self.window, 
                                text="Nhập vị trí cột (0-7) cho các hàng bạn đã biết:\n• Để trống nếu không biết vị trí\n• Chỉ nhập số từ 0 đến 7",
                                font=("Arial", 11),
                                justify=tk.CENTER,
                                fg="#555555")
        explain_label.pack(pady=10)
        
        # Frame cho bảng nhập liệu
        table_frame = tk.Frame(self.window)
        table_frame.pack(pady=15)
        
        # Tiêu đề bảng
        header_frame = tk.Frame(table_frame)
        header_frame.pack()
        
        tk.Label(header_frame, text="Hàng", width=8, font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="Cột", width=8, font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="", width=15).pack(side=tk.LEFT)  # placeholder
        
        # Tạo bảng nhập liệu
        self.entries = {}
        for i in range(self.n):
            row_frame = tk.Frame(table_frame)
            row_frame.pack(pady=4)
            
            tk.Label(row_frame, text=f"{i}", width=8, font=("Arial", 10)).pack(side=tk.LEFT)
            entry = tk.Entry(row_frame, width=8, font=("Arial", 10), justify=tk.CENTER, bg="#F8F9FA")
            entry.pack(side=tk.LEFT, padx=5)
            self.entries[i] = entry
            
            # Hiển thị trạng thái
            status_label = tk.Label(row_frame, text="(chưa nhập)", font=("Arial", 9), fg="#888888", width=15)
            status_label.pack(side=tk.LEFT)
            
            # Liên kết sự kiện thay đổi
            entry.bind('<KeyRelease>', lambda e, row=i, label=status_label: self.update_status(row, label))
        
        # Frame cho các tùy chọn nhanh
        quick_frame = tk.Frame(self.window)
        quick_frame.pack(pady=20)
        
        tk.Label(quick_frame, text="Tùy chọn nhanh:", font=("Arial", 12, "bold")).pack()
        
        quick_btn_frame = tk.Frame(quick_frame)
        quick_btn_frame.pack(pady=8)
        
        tk.Button(quick_btn_frame, text="Dễ - 1 quân hậu", 
                 command=lambda: self.set_difficulty("easy"),
                 bg="#28A745", fg="white", font=("Arial", 10),
                 width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(quick_btn_frame, text="Trung bình - 2 quân hậu", 
                 command=lambda: self.set_difficulty("medium"),
                 bg="#FFC107", fg="black", font=("Arial", 10),
                 width=18).pack(side=tk.LEFT, padx=5)
        
        tk.Button(quick_btn_frame, text="Khó - 3 quân hậu", 
                 command=lambda: self.set_difficulty("hard"),
                 bg="#DC3545", fg="white", font=("Arial", 10),
                 width=15).pack(side=tk.LEFT, padx=5)
        
        # Nút điều khiển
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="🔍 BẮT ĐẦU TÌM KIẾM", 
                 command=self.confirm,
                 bg="#2E86AB", fg="white", font=("Arial", 12, "bold"),
                 width=20, height=2).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="❌ HỦY", 
                 command=self.cancel,
                 bg="#6C757D", fg="white", font=("Arial", 11),
                 width=10, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🗑️ XÓA TẤT CẢ", 
                 command=self.clear_all,
                 bg="#FD7E14", fg="white", font=("Arial", 11),
                 width=12, height=2).pack(side=tk.LEFT, padx=5)
    
    def update_status(self, row, label):
        """Cập nhật trạng thái khi người dùng nhập liệu"""
        value = self.entries[row].get().strip()
        if value:
            if value.isdigit() and 0 <= int(value) < self.n:
                label.config(text="✓ đã nhập", fg="#28A745")
            else:
                label.config(text="❌ lỗi", fg="#DC3545")
        else:
            label.config(text="(chưa nhập)", fg="#888888")
    
    def set_difficulty(self, difficulty):
        """Thiết lập độ khó"""
        from part_infor import generate_smart_partial_goal
        self.partial_goal = generate_smart_partial_goal(self.n, difficulty)
        self.update_entries()
        
        # Hiển thị thông báo
        num_queens = len(self.partial_goal)
        messagebox.showinfo("Thiết lập độ khó", 
                           f"Đã thiết lập {difficulty.upper()}:\n{num_queens} quân hậu đã được cố định")
    
    def update_entries(self):
        """Cập nhật các ô nhập liệu từ partial goal"""
        # Xóa tất cả các ô nhập liệu trước
        self.clear_all()
        
        # Điền các giá trị từ partial goal
        for row, col in self.partial_goal.items():
            self.entries[row].delete(0, tk.END)
            self.entries[row].insert(0, str(col))
    
    def clear_all(self):
        """Xóa tất cả các ô nhập liệu"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.partial_goal = {}
    
    def confirm(self):
        """Xác nhận nhập liệu và bắt đầu tìm kiếm"""
        self.partial_goal = {}
        has_error = False
        error_message = ""
        
        for row, entry in self.entries.items():
            value = entry.get().strip()
            if value:
                try:
                    col = int(value)
                    if 0 <= col < self.n:
                        self.partial_goal[row] = col
                    else:
                        error_message = f"Lỗi: Cột phải trong khoảng 0-{self.n-1} (hàng {row})"
                        has_error = True
                        break
                except ValueError:
                    error_message = f"Lỗi: Giá trị ở hàng {row} phải là số nguyên"
                    has_error = True
                    break
        
        if has_error:
            messagebox.showerror("Lỗi nhập liệu", error_message)
            return
        
        if len(self.partial_goal) == 0:
            # Nếu không nhập gì, hỏi người dùng
            result = messagebox.askyesno("Xác nhận", 
                                        "Bạn chưa nhập thông tin nào.\n\nCó muốn sử dụng thiết lập mặc định (2 quân hậu) không?")
            if result:
                from part_infor import generate_smart_partial_goal
                self.partial_goal = generate_smart_partial_goal(self.n, "medium")
            else:
                return
        
        print(f"Thông tin đã nhập: {self.partial_goal}")
        messagebox.showinfo("Thông tin", f"Bắt đầu tìm kiếm với {len(self.partial_goal)} quân hậu đã biết!")
        self.window.destroy()
        
        # Gọi callback để chạy thuật toán
        if self.result_callback:
            self.result_callback(self.partial_goal)
    
    def cancel(self):
        """Hủy bỏ"""
        self.partial_goal = None
        self.window.destroy()
        messagebox.showinfo("Hủy", "Đã hủy nhập thông tin")
    
    def set_callback(self, callback):
        """Thiết lập callback khi hoàn thành"""
        self.result_callback = callback

def open_part_info_ui(parent, callback):
    """Mở giao diện Part Information UI"""
    ui = PartInfoUI(parent)
    ui.set_callback(callback)
    return ui