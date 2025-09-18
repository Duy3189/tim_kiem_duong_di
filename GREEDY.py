from queue import PriorityQueue
import kiem_tra_an_toan as at

def h(state):
    """Hàm heuristic: số cặp quân hậu xung đột"""
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts


def greedy():
    pq = PriorityQueue()
    pq.put((0, []))   # (h(x), trạng thái bàn cờ)
    states = []       # lưu tất cả trạng thái đã duyệt

    while not pq.empty():
        cost, board = pq.get()
        states.append(list(board))

        row = len(board)
        if row == 8:                 # nếu đủ 8 quân hậu
            if h(board) == 0:        # và không xung đột
                return board, states # trả về nghiệm và toàn bộ states
            continue

        # thử đặt hậu ở các cột trong hàng hiện tại
        for col in range(8):
            if at.is_safe(board, row, col):   # kiểm tra an toàn
                new_state = board + [col]
                new_cost = h(new_state)       # dùng h(x) cho Greedy
                pq.put((new_cost, new_state))

    return None, states  # nếu không tìm thấy nghiệm
