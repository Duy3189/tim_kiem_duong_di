import tkinter as tk
from PIL import Image, ImageTk

class Chess:
    def __init__(self, root, cell_size=60):
        self.root = root
        self.cell_size = cell_size
        self.queen_img = Image.open("queen.png").resize((cell_size-10, cell_size-10))
        self.queen = ImageTk.PhotoImage(self.queen_img)

        # tạo ra bàn cờ
        self.canvas1 = tk.Canvas(root, width=cell_size*8, height=cell_size*8)
        self.canvas2 = tk.Canvas(root, width=cell_size*8, height=cell_size*8)

        self.canvas1.grid(row=0, column=0, padx=30, pady=30)
        self.canvas2.grid(row=0, column=1, padx=30, pady=30)

        # tạo ra nhãn trên bàn cờ
        label1 = tk.Label(root, text="Quá trình thuật toán", font=("Arial", 16, "bold"))
        label1.grid(row=1, column=0)
        label2 = tk.Label(root, text="Kết quả cuối cùng", font=("Arial", 16, "bold"))
        label2.grid(row=1, column=1) 

        # lưu địa chỉ của hậu
        self.queen_list1 = []   # trạng thái trung gian
        self.queen_list2 = []   # kết quả cuối

        # vẽ bàn cờ trống
        self.trang_thai(self.canvas1)
        self.trang_thai(self.canvas2)

    def mau_sac(self, i, j):
        return "green" if (i+j) % 2 == 1 else "white"
        
    def trang_thai(self, canvas):
        """vẽ bàn cờ trống"""
        for i in range(8):
            for j in range(8):
                canvas.create_rectangle(
                    j*self.cell_size, i*self.cell_size,
                    (j+1)*self.cell_size, (i+1)*self.cell_size,
                    fill=self.mau_sac(i, j)
                )

    def hien_thi_trang_thai_trung_gian(self, board):
        """Hiển thị trạng thái trung gian (canvas trái)"""
        # xóa hết hậu cũ
        for q in self.queen_list1:
            self.canvas1.delete(q)
        self.queen_list1.clear()

        # vẽ hậu mới
        for i in range(len(board)):
            j = board[i]
            x = j*self.cell_size + self.cell_size//2
            y = i*self.cell_size + self.cell_size//2
            qid = self.canvas1.create_image(x, y, image=self.queen)
            self.queen_list1.append(qid)

    def hien_thi_ket_qua(self, board):
        """Hiển thị kết quả cuối cùng (canvas phải)"""
        # xóa hết hậu cũ
        for q in self.queen_list2:
            self.canvas2.delete(q)
        self.queen_list2.clear()

        # vẽ hậu mới
        for i in range(len(board)):
            j = board[i]
            x = j*self.cell_size + self.cell_size//2
            y = i*self.cell_size + self.cell_size//2
            qid = self.canvas2.create_image(x, y, image=self.queen)
            self.queen_list2.append(qid)