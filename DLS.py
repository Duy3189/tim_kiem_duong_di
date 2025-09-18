import kiem_tra_an_toan as at

cutoff = "cutoff"

def recursive_DLS(board, limit, visited_states):
    # lưu lại snapshot hiện tại
    visited_states.append(board[:])

    # Nếu đặt đủ 8 hậu thì trả kết quả
    if len(board) == 8:
        return board[:], visited_states

    # Hết giới hạn mà chưa đủ
    if limit == 0:
        return cutoff, visited_states

    cutoff_occurred = False
    for col in range(8):
        if at.is_safe(board, len(board), col):
            result, visited_states = recursive_DLS(board + [col], limit-1, visited_states)

            if result != cutoff and result is not None:
                return result, visited_states
            elif result == cutoff:
                cutoff_occurred = True

    return (cutoff if cutoff_occurred else None), visited_states


def DLS(limit=8):
    board = []
    visited_states = []
    result, visited_states = recursive_DLS(board, limit, visited_states)

    # chuẩn hóa output
    if result == cutoff or result is None:
        return None, visited_states
    return result, visited_states
