from DLS import recursive_DLS, cutoff

def IDS(max_depth=8):
    """
    Tìm kiếm lặp sâu dần (IDS).
    Trả về (final_path, visited_states).
    """
    for depth in range(max_depth + 1):
        board = []
        visited_states = []
        result, visited_states = recursive_DLS(board, depth, visited_states)

        if result == cutoff or result is None:
            continue   # chưa tìm thấy, thử tăng giới hạn sâu
        else:
            return result, visited_states  # final_path + visited_states

    return None, []  # không tìm thấy
