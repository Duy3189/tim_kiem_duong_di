from collections import deque
from typing import List, Dict, Tuple, Any
import random

class PartInformationProblem:
    def __init__(self, n=8, partial_goal=None):
        self.n = n
        self.partial_goal = partial_goal if partial_goal is not None else {}
        self.initial_states = self.generate_initial_states()
        self.goal_states = self.generate_goal_space()
    
    def generate_initial_states(self) -> List[List[int]]:
        if not self.partial_goal:
            return [[col] for col in range(self.n)]
        
        initial_states = []
        if 0 in self.partial_goal:
            initial_states.append([self.partial_goal[0]])
        else:
            for col in range(self.n):
                if self.is_safe_partial([col], 0, col):
                    initial_states.append([col])
        return initial_states
    
    def generate_goal_space(self) -> List[List[int]]:
        goal_states = []
        stack = [[]]
        
        while stack:
            state = stack.pop()
            row = len(state)
            
            if row == self.n:
                if self.is_valid_solution(state) and self.satisfies_partial_goal(state):
                    goal_states.append(state.copy())
                continue
            
            if row in self.partial_goal:
                col = self.partial_goal[row]
                if self.is_safe(state, row, col):
                    new_state = state + [col]
                    stack.append(new_state)
            else:
                for col in range(self.n):
                    if self.is_safe(state, row, col):
                        new_state = state + [col]
                        stack.append(new_state)
        return goal_states
    
    def is_safe(self, state: List[int], row: int, col: int) -> bool:
        for r, c in enumerate(state):
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True
    
    def is_safe_partial(self, state: List[int], row: int, col: int) -> bool:
        for r, c in enumerate(state):
            if c == col or abs(c - col) == abs(r - row):
                return False
        
        for r, c in self.partial_goal.items():
            if r != row:
                if c == col or abs(c - col) == abs(r - row):
                    return False
        return True
    
    def satisfies_partial_goal(self, state: List[int]) -> bool:
        for row, col in self.partial_goal.items():
            if row < len(state) and state[row] != col:
                return False
        return True
    
    def is_valid_solution(self, state: List[int]) -> bool:
        n = len(state)
        for i in range(n):
            for j in range(i + 1, n):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    return False
        return True
    
    def is_goal(self, state: List[int]) -> bool:
        return (len(state) == self.n and 
                self.is_valid_solution(state) and 
                self.satisfies_partial_goal(state))
    
    def actions(self, state: List[int]) -> List[int]:
        row = len(state)
        if row >= self.n:
            return []
        
        if row in self.partial_goal:
            col = self.partial_goal[row]
            if self.is_safe(state, row, col):
                return [col]
            return []
        
        actions = []
        for col in range(self.n):
            if self.is_safe(state, row, col):
                actions.append(col)
        return actions
    
    def result(self, state: List[int], action: int) -> List[int]:
        return state + [action]

def part_information_bfs_search(problem: PartInformationProblem) -> Tuple[List[List[int]], List[List[int]]]:
    visited_states = []
    solutions = []
    
    frontier = deque()
    for initial_state in problem.initial_states:
        frontier.append(initial_state)
        visited_states.append(initial_state)
    
    while frontier:
        current_state = frontier.popleft()
        
        if problem.is_goal(current_state):
            if current_state not in solutions:
                solutions.append(current_state)
            continue
        
        possible_actions = problem.actions(current_state)
        
        for action in possible_actions:
            new_state = problem.result(current_state, action)
            
            if new_state not in visited_states:
                visited_states.append(new_state)
                frontier.append(new_state)
    
    return solutions, visited_states

def generate_smart_partial_goal(n=8, difficulty="medium"):
    """Tạo partial goal thông minh - FIXED không import BFS"""
    # Tạo một nghiệm hợp lệ cố định thay vì import BFS
    # Đây là một nghiệm hợp lệ của bài toán 8 hậu
    valid_solution = [0, 4, 7, 5, 2, 6, 1, 3]
    
    if difficulty == "easy":
        num_fixed = 1
    elif difficulty == "medium":
        num_fixed = 2
    else:  # hard
        num_fixed = 3
    
    rows = random.sample(range(n), num_fixed)
    partial_goal = {}
    
    for row in rows:
        partial_goal[row] = valid_solution[row]
    
    return partial_goal

def partial_goal_main_bfs(n=8, partial_goal=None):
    """Hàm chính cho Part Information Search"""
    try:
        if partial_goal is None:
            partial_goal = generate_smart_partial_goal(n, "medium")
        
        print(f"🎯 Bắt đầu tìm kiếm với Partial Goal: {partial_goal}")
        
        problem = PartInformationProblem(n, partial_goal)
        solutions, visited_states = part_information_bfs_search(problem)
        
        print(f"📊 Kết quả:")
        print(f"   - Không gian ban đầu: {len(problem.initial_states)} states")
        print(f"   - Không gian đích: {len(problem.goal_states)} goal states") 
        print(f"   - Tìm thấy {len(solutions)} nghiệm")
        
        if solutions:
            final_solution = solutions[0]
            print(f"   - Nghiệm đầu tiên: {final_solution}")
            
            # Tạo danh sách states để hiển thị
            display_states = []
            
            # Thêm các visited states
            for state in visited_states:
                if state not in display_states:
                    display_states.append(state)
            
            # Đảm bảo final solution có trong display_states
            if final_solution not in display_states:
                display_states.append(final_solution)
            
            print(f"   - Số bước hiển thị: {len(display_states)}")
            return final_solution, display_states
        else:
            print("❌ Không tìm thấy nghiệm thỏa mãn partial goal")
            return [], []
            
    except Exception as e:
        print(f"💥 Lỗi trong Part Information Search: {e}")
        import traceback
        traceback.print_exc()
        return [], []