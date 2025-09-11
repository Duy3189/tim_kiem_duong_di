import kiem_tra_an_toan as at
def dfs(board=None, states=None):
    if board is None:
        board = []
    if states is None:
        states = []

    states.append(board)

    row = len(board)
    if row == 8:
        return states

    for col in range(8):
        if at.is_safe(board, row, col):
            result = dfs(board + [col], states)
            if len(result[-1]) == 8:  # dừng khi tìm được nghiệm
                return result

    return states
