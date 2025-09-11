def is_safe(board, row, col):
    """Kiểm tra xem có đặt được hậu ở (row, col) không"""
    for i in range(row):
        # cùng cột hoặc chéo nhau
        if board[i] == col or abs(board[i] - col) == abs(i - row):
            return False
    return True
