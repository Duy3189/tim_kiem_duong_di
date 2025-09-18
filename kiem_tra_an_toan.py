def is_safe(board, row, col):
    """
    Kiểm tra có thể đặt hậu tại (row, col) không
    board[i] = cột của hậu ở hàng i
    """
    for i in range(len(board)):
        if board[i] == col or abs(board[i] - col) == abs(i - row):
            return False
    return True
