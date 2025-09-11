#tạo ra hàm bfs trả về trạng thái tìm được
from collections import deque
import kiem_tra_an_toan as at

def bfs():
    queue = deque()          # tạo hàng đợi
    queue.append([])         # trạng thái ban đầu: bàn cờ trống
    states = []              # lưu toàn bộ trạng thái đã duyệt

    while queue:
        board = queue.popleft()   # lấy trạng thái ra khỏi hàng đợi
        states.append(board)      # lưu lại

        row = len(board)          # số hàng đã đặt hậu
        if row == 8:              # đủ 8 hàng -> nghiệm
            return states
        
        for col in range(8):      # thử đặt hậu ở tất cả các cột
            if at.is_safe(board, row, col):
                queue.append(board + [col])
    
    return states
