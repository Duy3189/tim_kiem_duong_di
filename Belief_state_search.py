import kiem_tra_an_toan as at

visited_beliefs = []  # Lưu các belief states đã thăm

class Problem:
    def __init__(self, n=8):
        self.n = n
        # initial belief state: có thể bắt đầu từ bất kỳ vị trí nào ở hàng 0
        self.initial = [[]]  # belief state ban đầu gồm 1 trạng thái rỗng

    def is_goal(self, state):
        return len(state) == self.n   # đủ 8 quân hậu

    def actions(self, state):
        """Trả về các cột khả thi cho 1 state"""
        row = len(state)
        acts = []
        for col in range(self.n):
            if at.is_safe(state, row, col):
                acts.append(col)
        return acts

    def results(self, state, action):
        """Trả về danh sách state mới sau khi áp dụng action"""
        return [state + [action]]


def belief_state_search(problem):
    # initial belief state: tập hợp các trạng thái hiện tại
    initial_belief = problem.initial
    return or_search_belief(problem, initial_belief, [])


def or_search_belief(problem, belief_state, path):
    visited_beliefs.append([s.copy() for s in belief_state])  # lưu copy của belief state

    # goal test: nếu mọi state trong belief state đạt goal
    if all(problem.is_goal(s) for s in belief_state):
        return []  # kế hoạch trống khi đạt goal

    # tránh chu trình
    if belief_state in path:
        return None

    # thử từng action khả thi (dựa trên tập belief)
    actions_set = set()
    for s in belief_state:
        actions_set.update(problem.actions(s))
    actions_list = list(actions_set)

    for action in actions_list:
        # áp dụng action cho tất cả các state trong belief
        new_belief = []
        for s in belief_state:
            results = problem.results(s, action)
            new_belief.extend(results)
        plan = and_search_belief(problem, new_belief, path + [belief_state])
        if plan is not None:
            return [(action, plan)]
    return None


def and_search_belief(problem, belief_states, path):
    plan_dict = {}
    for s in belief_states:
        plan_s = or_search_belief(problem, [s], path)
        if plan_s is None:
            return None
        plan_dict[tuple(s)] = plan_s
    return plan_dict


def belief_state_main():
    """Hàm gọi chính để tích hợp UI"""
    global visited_beliefs
    visited_beliefs = []  # reset

    problem = Problem(8)
    plan = belief_state_search(problem)

    # tìm state cuối cùng đạt goal
    final_state = None
    for belief in visited_beliefs:
        for s in belief:
            if len(s) == problem.n:
                final_state = s
                break
        if final_state:
            break

    return final_state, visited_beliefs
