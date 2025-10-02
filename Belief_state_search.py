from collections import deque
from typing import List, Any, Tuple

class BeliefStateProblem:
    def __init__(self, n=8):
        self.n = n
    
    def generate_initial_belief(self) -> List[List[int]]:
        """Tạo belief state ban đầu"""
        return [[col] for col in range(self.n)]
    
    def is_goal(self, belief_state: List[List[int]]) -> bool:
        """Kiểm tra belief state có thỏa mãn điều kiện đích không"""
        if not belief_state:
            return False
        for state in belief_state:
            if len(state) != self.n or not self.is_valid_solution(state):
                return False
        return True
    
    def is_valid_solution(self, state: List[int]) -> bool:
        """Kiểm tra state có phải là nghiệm hợp lệ"""
        n = len(state)
        for i in range(n):
            for j in range(i + 1, n):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    return False
        return True
    
    def is_safe(self, state: List[int], row: int, col: int) -> bool:
        """Kiểm tra đặt hậu tại (row, col) có an toàn không"""
        for r, c in enumerate(state):
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True
    
    def actions(self, belief_state: List[List[int]]) -> List[int]:
        """Lấy tất cả hành động có thể từ belief state"""
        if not belief_state:
            return []
        
        row = len(belief_state[0])
        if row >= self.n:
            return []
        
        all_actions = set()
        for state in belief_state:
            for col in range(self.n):
                if self.is_safe(state, row, col):
                    all_actions.add(col)
        return list(all_actions)
    
    def result(self, belief_state: List[List[int]], action: int) -> List[List[int]]:
        """Áp dụng hành động lên belief state"""
        new_belief = []
        row = len(belief_state[0]) if belief_state else 0
        
        for state in belief_state:
            if self.is_safe(state, row, action):
                new_state = state + [action]
                new_belief.append(new_state)
        
        return new_belief
    
    def belief_equal(self, belief1: List[List[int]], belief2: List[List[int]]) -> bool:
        """So sánh hai belief state có bằng nhau không"""
        if len(belief1) != len(belief2):
            return False
        set1 = set(tuple(state) for state in belief1)
        set2 = set(tuple(state) for state in belief2)
        return set1 == set2

def belief_state_bfs_search(problem: BeliefStateProblem) -> Tuple[List[List[int]], List[List[List[int]]]]:
    """Thực hiện BFS trên không gian belief states"""
    visited_beliefs = []
    frontier = deque([(problem.generate_initial_belief(), [])])
    solutions = []
    
    while frontier:
        current_belief, path = frontier.popleft()
        visited_beliefs.append(current_belief)
        
        # Kiểm tra điều kiện đích
        if problem.is_goal(current_belief):
            for state in current_belief:
                if problem.is_valid_solution(state):
                    solutions.append(state)
            break
        
        # Lấy tất cả hành động có thể
        possible_actions = problem.actions(current_belief)
        
        for action in possible_actions:
            new_belief = problem.result(current_belief, action)
            if new_belief:
                new_path = path + [action]
                # Kiểm tra belief state mới chưa được visited
                is_visited = False
                for visited in visited_beliefs:
                    if problem.belief_equal(new_belief, visited):
                        is_visited = True
                        break
                
                if not is_visited:
                    frontier.append((new_belief, new_path))
    
    return solutions, visited_beliefs

def belief_state_main(n=8):
    """Hàm chính cho Belief State Search"""
    try:
        problem = BeliefStateProblem(n)
        solutions, visited_beliefs = belief_state_bfs_search(problem)
        
        if solutions:
            final_solution = solutions[0]
            
            # Tạo danh sách states để hiển thị
            display_states = []
            
            # Lấy representative state từ mỗi belief
            for belief in visited_beliefs:
                if belief:
                    # Thêm các state từ belief
                    for state in belief:
                        for i in range(1, len(state) + 1):
                            partial = state[:i]
                            if partial not in display_states:
                                display_states.append(partial)
            
            # Đảm bảo final solution có trong display_states
            if final_solution not in display_states:
                display_states.append(final_solution)
                
            print(f"Belief State Search: Tìm thấy {len(solutions)} nghiệm")
            return final_solution, display_states
        else:
            print("Belief State Search: Không tìm thấy nghiệm")
            return [], []
            
    except Exception as e:
        print(f"Lỗi trong Belief State Search: {e}")
        return [], []