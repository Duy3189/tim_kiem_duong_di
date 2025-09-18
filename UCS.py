from queue import PriorityQueue
import kiem_tra_an_toan as at

def dem(i, j):
    """Hàm tính chi phí đặt hậu ở (i, j)."""
    if (i == 0) or (i == 7) or (j == 7) or (j == 0):
        return 1
    elif (i == 1) or (j == 1) or (i == 6) or (j == 6):
        return 2
    elif (i == 2) or (j == 2) or (i == 5) or (j == 5):
        return 3
    else:
        return 4

def ucs():
    """
    Uniform Cost Search cho bài toán 8 quân hậu.
    Trả về (final_path, visited_states).
    """
    pq = PriorityQueue()
    pq.put((0, []))   # (tổng chi phí, trạng thái bàn cờ)
    visited_states = []   # lưu toàn bộ trạng thái duyệt

    while not pq.empty():
        cost, board = pq.get()
        visited_states.append(list(board))   # copy để tránh tham chiếu

        row = len(board)
        if row == 8:   # nếu đủ 8 quân hậu => nghiệm
            return board, visited_states  # final_path, visited_states

        # thử đặt hậu ở các cột
        for col in range(8):
            if at.is_safe(board, row, col):
                new_cost = cost + dem(row, col)
                pq.put((new_cost, board + [col]))

    return None, visited_states  # không tìm thấy
