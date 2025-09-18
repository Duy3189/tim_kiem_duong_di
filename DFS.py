import kiem_tra_an_toan as at

def dfs(board=None, visited_states=None):
    if board is None:
        board = []
    if visited_states is None:
        visited_states = []

    # lưu lại trạng thái hiện tại
    visited_states.append(board[:])

    row = len(board)
    if row == 8:  # đủ 8 hàng -> nghiệm
        final_path = board[:]
        return final_path, visited_states

    for col in range(8):
        if at.is_safe(board, row, col):
            final_path, visited_states = dfs(board + [col], visited_states)
            if final_path:  # nếu tìm được nghiệm
                return final_path, visited_states

    return None, visited_states
