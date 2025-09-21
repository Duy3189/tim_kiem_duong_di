import random

def h(state):
    """Heuristic: số cặp hậu không tấn công nhau"""
    n = len(state)
    non_conflict = 0
    total_pairs = n * (n - 1) // 2
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    non_conflict = total_pairs - conflicts
    return non_conflict


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


def hill_climbing(n=8):
    visited_states = []

    # Khởi tạo ngẫu nhiên
    current = [random.randint(0, n-1) for _ in range(n)]
    visited_states.append(list(current))  # lưu trạng thái đầu tiên

    while True:
        E = h(current)
        neighbors = get_neighbors(current)

        # Tính h cho tất cả neighbor
        scores = [(h(nb), nb) for nb in neighbors]

        # Lấy neighbor tốt nhất
        best_score, best_neighbor = max(scores, key=lambda x: x[0])

        if best_score > E:   # cải thiện
            current = best_neighbor
            visited_states.append(list(current))  # lưu lại trạng thái
        else:                # không cải thiện nữa
            return current, visited_states
