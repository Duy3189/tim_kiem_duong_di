from typing import List, Dict, Set, Tuple, Optional
import time

class CSPProblem:
    def __init__(self, n=8):
        self.n = n
        self.variables = list(range(n))  # Các hàng (0 đến n-1)
        self.domains = {i: set(range(n)) for i in range(n)}  # Domain ban đầu: tất cả các cột
    
    def is_consistent(self, assignment: Dict[int, int], var: int, value: int) -> bool:
        """Kiểm tra tính nhất quán khi gán value cho var"""
        for row, col in assignment.items():
            if row == var:
                continue
            # Kiểm tra cùng cột hoặc cùng đường chéo
            if col == value or abs(col - value) == abs(row - var):
                return False
        return True
    
    def get_unassigned_variable(self, assignment: Dict[int, int]) -> Optional[int]:
        """Lấy biến chưa được gán"""
        for var in self.variables:
            if var not in assignment:
                return var
        return None

def backtracking_search(problem: CSPProblem) -> Tuple[Optional[List[int]], List[List[int]]]:
    """Thuật toán Backtracking cho CSP"""
    visited_states = []
    
    def backtrack(assignment: Dict[int, int]) -> Optional[Dict[int, int]]:
        # Thêm trạng thái hiện tại vào visited
        current_state = [assignment.get(i, -1) for i in range(problem.n)]
        visited_states.append(current_state)
        
        # Kiểm tra nếu đã gán hết tất cả biến
        if len(assignment) == problem.n:
            return assignment
        
        # Chọn biến chưa được gán
        var = problem.get_unassigned_variable(assignment)
        
        # Thử các giá trị trong domain của biến
        for value in problem.domains[var]:
            if problem.is_consistent(assignment, var, value):
                assignment[var] = value
                result = backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]
        
        return None
    
    assignment = {}
    result = backtrack(assignment)
    
    if result:
        # Chuyển từ dict sang list
        solution = [result[i] for i in range(problem.n)]
        return solution, visited_states
    else:
        return None, visited_states

def forward_checking_search(problem: CSPProblem) -> Tuple[Optional[List[int]], List[List[int]]]:
    """Thuật toán Forward Checking cho CSP"""
    visited_states = []
    
    def forward_check(assignment: Dict[int, int], domains: Dict[int, Set[int]]) -> bool:
        """Thực hiện forward checking và trả về False nếu có domain rỗng"""
        current_var = max(assignment.keys()) if assignment else -1
        
        for var in domains:
            if var in assignment:
                continue
                
            to_remove = set()
            for value in domains[var]:
                if not problem.is_consistent(assignment, var, value):
                    to_remove.add(value)
            
            domains[var] -= to_remove
            if not domains[var]:
                return False
        
        return True
    
    def fc_backtrack(assignment: Dict[int, int], domains: Dict[int, Set[int]]) -> Optional[Dict[int, int]]:
        # Thêm trạng thái hiện tại vào visited
        current_state = [assignment.get(i, -1) for i in range(problem.n)]
        visited_states.append(current_state)
        
        # Kiểm tra nếu đã gán hết tất cả biến
        if len(assignment) == problem.n:
            return assignment
        
        # Chọn biến chưa được gán (MRV - Minimum Remaining Values)
        unassigned_vars = [var for var in problem.variables if var not in assignment]
        var = min(unassigned_vars, key=lambda x: len(domains[x]))
        
        # Lưu domain hiện tại để backup
        domains_backup = {v: domains[v].copy() for v in domains}
        
        # Thử các giá trị trong domain của biến
        for value in list(domains[var]):
            if problem.is_consistent(assignment, var, value):
                assignment[var] = value
                
                # Tạo domains mới và thực hiện forward checking
                new_domains = {v: domains[v].copy() for v in domains}
                
                if forward_check(assignment, new_domains):
                    result = fc_backtrack(assignment, new_domains)
                    if result is not None:
                        return result
                
                # Quay lui: khôi phục assignment và domains
                del assignment[var]
                domains.update(domains_backup)
        
        return None
    
    # Khởi tạo domains
    domains = {i: problem.domains[i].copy() for i in problem.variables}
    assignment = {}
    
    result = fc_backtrack(assignment, domains)
    
    if result:
        # Chuyển từ dict sang list
        solution = [result[i] for i in range(problem.n)]
        return solution, visited_states
    else:
        return None, visited_states

def backtracking_main(n=8):
    """Hàm chính cho Backtracking"""
    try:
        print("🔍 Đang chạy Backtracking Search...")
        problem = CSPProblem(n)
        solution, visited_states = backtracking_search(problem)
        
        if solution:
            print(f"✅ Backtracking: Tìm thấy nghiệm")
            print(f"   - Số bước: {len(visited_states)}")
            print(f"   - Nghiệm: {solution}")
            
            # Lọc các state hợp lệ để hiển thị (bỏ các state có -1)
            display_states = []
            for state in visited_states:
                # Chỉ thêm state có ít nhất 1 quân hậu
                if any(x != -1 for x in state):
                    # Tạo partial state cho đến vị trí được gán cuối cùng
                    partial_state = []
                    for val in state:
                        if val == -1:
                            break
                        partial_state.append(val)
                    if partial_state and partial_state not in display_states:
                        display_states.append(partial_state)
            
            # Đảm bảo solution có trong display_states
            if solution not in display_states:
                display_states.append(solution)
                
            return solution, display_states
        else:
            print("❌ Backtracking: Không tìm thấy nghiệm")
            return [], []
            
    except Exception as e:
        print(f"💥 Lỗi trong Backtracking: {e}")
        import traceback
        traceback.print_exc()
        return [], []

def forward_checking_main(n=8):
    """Hàm chính cho Forward Checking"""
    try:
        print("🔍 Đang chạy Forward Checking Search...")
        problem = CSPProblem(n)
        solution, visited_states = forward_checking_search(problem)
        
        if solution:
            print(f"✅ Forward Checking: Tìm thấy nghiệm")
            print(f"   - Số bước: {len(visited_states)}")
            print(f"   - Nghiệm: {solution}")
            
            # Lọc các state hợp lệ để hiển thị
            display_states = []
            for state in visited_states:
                if any(x != -1 for x in state):
                    partial_state = []
                    for val in state:
                        if val == -1:
                            break
                        partial_state.append(val)
                    if partial_state and partial_state not in display_states:
                        display_states.append(partial_state)
            
            if solution not in display_states:
                display_states.append(solution)
                
            return solution, display_states
        else:
            print("❌ Forward Checking: Không tìm thấy nghiệm")
            return [], []
            
    except Exception as e:
        print(f"💥 Lỗi trong Forward Checking: {e}")
        import traceback
        traceback.print_exc()
        return [], []

# Hàm so sánh hiệu năng
def compare_csp_algorithms(n=8):
    """So sánh hiệu năng giữa Backtracking và Forward Checking"""
    print("\n" + "="*50)
    print("SO SÁNH HIỆU NĂNG CSP ALGORITHMS")
    print("="*50)
    
    # Backtracking
    start_time = time.time()
    problem1 = CSPProblem(n)
    solution1, states1 = backtracking_search(problem1)
    bt_time = time.time() - start_time
    
    # Forward Checking
    start_time = time.time()
    problem2 = CSPProblem(n)
    solution2, states2 = forward_checking_search(problem2)
    fc_time = time.time() - start_time
    
    print(f"Backtracking:")
    print(f"  - Thời gian: {bt_time:.4f} giây")
    print(f"  - Số bước: {len(states1)}")
    print(f"  - Nghiệm: {solution1}")
    
    print(f"\nForward Checking:")
    print(f"  - Thời gian: {fc_time:.4f} giây")
    print(f"  - Số bước: {len(states2)}")
    print(f"  - Nghiệm: {solution2}")
    
    print(f"\nForward Checking nhanh hơn {bt_time/fc_time:.2f} lần")
    print(f"Forward Checking ít hơn {len(states1)/len(states2):.2f} lần số bước")

if __name__ == "__main__":
    # Test các thuật toán
    compare_csp_algorithms(8)