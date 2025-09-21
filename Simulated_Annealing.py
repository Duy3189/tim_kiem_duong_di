import random
import math

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


def random_neighbor(state):
    """Sinh ra một neighbor ngẫu nhiên"""
    n = len(state)
    row = random.randint(0, n-1)
    col = random.randint(0, n-1)
    while col == state[row]:
        col = random.randint(0, n-1)
    new_state = list(state)
    new_state[row] = col
    return new_state


def simulated_annealing(n=8, T=100.0, alpha=0.95, max_iter=1000):
    visited_states = []

    # khởi tạo ngẫu nhiên
    current = [random.randint(0, n-1) for _ in range(n)]
    visited_states.append(list(current))

    for _ in range(max_iter):
        E = h(current)
        if E == n * (n - 1) // 2:   # tìm thấy lời giải tối ưu
            return current, visited_states

        # chọn neighbor ngẫu nhiên
        neighbor = random_neighbor(current)
        E_neighbor = h(neighbor)

        if E_neighbor >= E:
            current = neighbor
        else:
            # xác suất nhận neighbor kém hơn
            p = math.exp((E_neighbor - E) / T)
            if random.random() < p:
                current = neighbor

        visited_states.append(list(current))
        T = alpha * T   # giảm nhiệt độ

        if T < 1e-3:    # dừng khi nhiệt độ quá thấp
            break

    return current, visited_states
