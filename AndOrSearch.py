import kiem_tra_an_toan as at

visited_states = []  # Lưu đường đi

class Problem:
    def __init__(self, n=8):
        self.n = n
        self.initial = []

    def is_goal(self, state):
        return len(state) == self.n   # đủ 8 quân hậu

    def actions(self, state):
        row = len(state)
        acts = []
        for col in range(self.n):
            if at.is_safe(state, row, col):
                acts.append(col)
        return acts

    def results(self, state, action):
        # Tạm coi xác định: chỉ sinh 1 trạng thái mới
        return [state + [action]]

def and_or_search(problem):
    return or_search(problem, problem.initial, [])

def or_search(problem, state, path):
    visited_states.append(state.copy())   # Lưu state đã thăm

    if problem.is_goal(state):
        return []   # đạt goal
    if state in path:
        return None # thất bại do chu trình

    for action in problem.actions(state):
        plan = and_search(problem, problem.results(state, action), path + [state])
        if plan is not None:
            return [(action, plan)]
    return None

def and_search(problem, states, path):
    plan_dict = {}
    for s in states:
        plan_s = or_search(problem, s, path)
        if plan_s is None:
            return None
        plan_dict[tuple(s)] = plan_s
    return plan_dict

def and_or_main():
    """Hàm gọi chính để tích hợp vào UI"""
    global visited_states
    visited_states = []  # reset

    problem = Problem(8)
    plan = and_or_search(problem)

    # trạng thái cuối cùng chính là state đạt goal
    final_state = None
    for s in visited_states:
        if len(s) == problem.n:
            final_state = s
            break

    return final_state, visited_states
