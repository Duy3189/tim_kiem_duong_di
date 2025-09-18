from collections import deque
import kiem_tra_an_toan as at

def bfs():
    queue = deque()          # tạo hàng đợi
    queue.append([])         # trạng thái ban đầu: bàn cờ trống
    visited_states = []      # lưu toàn bộ trạng thái đã duyệt

    while queue:
        board = queue.popleft()   # lấy trạng thái ra khỏi hàng đợi
        visited_states.append(board[:])  # copy để lưu lại an toàn

        row = len(board)          # số hàng đã đặt hậu
        if row == 8:              # đủ 8 hàng -> nghiệm
            final_path = board[:] # copy nghiệm
            return final_path, visited_states
        
        # thử đặt hậu ở tất cả các cột
        for col in range(8):
            if at.is_safe(board, row, col):
                queue.append(board + [col])
    
    # nếu không tìm được nghiệm
    return None, visited_states
