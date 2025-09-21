import random

def h(state):
    """Heuristic: số cặp hậu không tấn công nhau"""
    n = len(state)
    total_pairs = n * (n - 1) // 2
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return total_pairs - conflicts


def get_neighbors(state):
    """Sinh ra tất cả neighbors bằng cách đổi vị trí cột của 1 quân hậu"""
    neighbors = []
    n = len(state)
    for row in range(n):
        for col in range(n):
            if state[row] != col:  # đổi sang cột khác
                new_state = list(state)
                new_state[row] = col
                neighbors.append(new_state)
    return neighbors


def beam_search(n=8, k=3, max_iter=1000):
    """
    Beam Search cho bài toán 8 quân hậu
    n: số quân hậu
    k: beam width
    """
    visited_states = []

    # khởi tạo k trạng thái ngẫu nhiên
    beam = [[random.randint(0, n-1) for _ in range(n)] for _ in range(k)]
    visited_states.extend([list(b) for b in beam])

    for _ in range(max_iter):
        # kiểm tra nghiệm tối ưu
        for state in beam:
            if h(state) == n * (n - 1) // 2:
                return state, visited_states

        # sinh neighbors từ toàn bộ beam
        all_neighbors = []
        for state in beam:
            all_neighbors.extend(get_neighbors(state))

        # sắp xếp theo heuristic giảm dần
        all_neighbors.sort(key=lambda s: h(s), reverse=True)

        # chọn top k trạng thái
        beam = all_neighbors[:k]
        visited_states.extend([list(b) for b in beam])

    # nếu không tìm ra nghiệm tối ưu thì trả về trạng thái tốt nhất
    best = max(beam, key=lambda s: h(s))
    return best, visited_states
