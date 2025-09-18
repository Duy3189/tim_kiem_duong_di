import tkinter as tk
from PIL import Image, ImageTk
import os


class Chess:
    def __init__(self, root, cell_size=60):
        self.root = root
        self.cell_size = cell_size

        # thử load ảnh queen, nếu không có thì fallback
        if os.path.exists("queen.png"):
            self.queen_img = Image.open("queen.png").resize((cell_size-10, cell_size-10))
            self.queen = ImageTk.PhotoImage(self.queen_img)
        else:
            self.queen = None

        # canvas trái = trạng thái trung gian
        self.canvas_left = tk.Canvas(root, width=cell_size*8, height=cell_size*8)
        self.canvas_left.grid(row=0, column=0, padx=30, pady=30)

        # canvas phải = kết quả cuối cùng
        self.canvas_right = tk.Canvas(root, width=cell_size*8, height=cell_size*8)
        self.canvas_right.grid(row=0, column=1, padx=30, pady=30)

        # label cho từng bàn cờ
        tk.Label(root, text="Trạng thái trung gian", font=("Arial", 16, "bold")).grid(row=1, column=0)
        tk.Label(root, text="Kết quả cuối cùng", font=("Arial", 16, "bold")).grid(row=1, column=1)

        # danh sách hậu
        self.queens_left = []
        self.queens_right = []

        # vẽ bàn cờ trống
        self._draw_board(self.canvas_left)
        self._draw_board(self.canvas_right)

    def _cell_color(self, i, j):
        """Màu ô bàn cờ (chuẩn cờ vua)"""
        return "#b58863" if (i+j) % 2 else "#f0d9b5"

    def _draw_board(self, canvas):
        for i in range(8):
            for j in range(8):
                canvas.create_rectangle(
                    j*self.cell_size, i*self.cell_size,
                    (j+1)*self.cell_size, (i+1)*self.cell_size,
                    fill=self._cell_color(i, j), outline=""
                )

    def _draw_queens(self, canvas, queens_list, board):
        """Xóa và vẽ lại quân hậu"""
        for q in queens_list:
            canvas.delete(q)
        queens_list.clear()

        # Nếu board là danh sách nhiều trạng thái thì lấy trạng thái cuối
        if board and isinstance(board[0], list):
            board = board[-1]

        # Chỉ vẽ nếu board là list các số nguyên
        if not all(isinstance(x, int) for x in board):
            return  

        for i, j in enumerate(board):
            x = j * self.cell_size + self.cell_size // 2
            y = i * self.cell_size + self.cell_size // 2
            if self.queen:
                qid = canvas.create_image(x, y, image=self.queen)
            else:
                qid = canvas.create_oval(
                    x - 20, y - 20, x + 20, y + 20,
                    fill="red", outline="black"
                )
            queens_list.append(qid)


    def hien_thi_trang_thai_trung_gian(self, board):
        self._draw_queens(self.canvas_left, self.queens_left, board)

    def hien_thi_ket_qua(self, board):
        self._draw_queens(self.canvas_right, self.queens_right, board)
