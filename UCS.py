from queue import PriorityQueue
import kiem_tra_an_toan as at

def dem(i, j):
    """Hàm tính chi phí đặt hậu ở (i, j)"""
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
    Trả về danh sách các trạng thái đã duyệt.
    """
    pq = PriorityQueue()
    pq.put((0, []))   # (tổng chi phí, trạng thái bàn cờ)
    states = []       # lưu toàn bộ trạng thái duyệt

    while not pq.empty():
        cost, board = pq.get()
        states.append(list(board))   # lưu lại bản copy

        row = len(board)             # số hàng đã đặt hậu
        if row == 8:                 # nếu đủ 8 quân hậu => trả về
            return states

        # thử đặt hậu ở các cột
        for col in range(8):
            if at.is_safe(board, row, col):   # kiểm tra an toàn
                new_cost = cost + dem(row, col)
                pq.put((new_cost, board + [col]))

    return states
