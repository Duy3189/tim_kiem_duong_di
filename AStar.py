from queue import PriorityQueue
import kiem_tra_an_toan as at

def count_safe_cells(board):
    """Đếm số ô an toàn có thể đặt hậu tiếp theo"""
    n = 8
    row = len(board)
    safe_cells = 0
    for r in range(row, n):
        for c in range(n):
            if at.is_safe(board, r, c):
                safe_cells += 1
    return safe_cells

def astar():
    pq = PriorityQueue()
    pq.put((0, []))   # (f(x), board)
    visited_states = []

    while not pq.empty():
        f, board = pq.get()
        visited_states.append(board.copy())

        row = len(board)
        if row == 8:   # đủ 8 quân hậu
            return board, visited_states   

        for col in range(8):
            if at.is_safe(board, row, col):
                new_board = board + [col]

                g = len(new_board)   # số quân đã đặt
                safe_cells = count_safe_cells(new_board)
                h = (8 - len(new_board)) + (20 - safe_cells) // 5
                f_new = g + h

                pq.put((f_new, new_board))

    return None, visited_states
