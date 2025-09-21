# Luu_duong_di.py
class DuongDi:
    def __init__(self):
        self.states = []       # tất cả trạng thái duyệt
        self.final_path = None # nghiệm cuối cùng
        self.index = 0

    def cap_nhat_states(self, states, final_path=None):
        """
        Cập nhật lại danh sách trạng thái và lời giải cuối.
        - states: visited_states
        - final_path: nghiệm cuối cùng (list 8 vị trí hậu)
        """
        self.states = states
        self.final_path = final_path
        self.index = 0

    def next_state(self):
        while self.index < len(self.states):
            state = self.states[self.index]
            self.index += 1
            if self.index == 1 or state != self.states[self.index - 2]:
                return state
        return None


    def get_final_state(self):
        """Trả về trạng thái cuối cùng (lời giải)"""
        if self.final_path:
            return self.final_path
        elif self.states:
            return self.states[-1]
        return None
