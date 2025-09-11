#hậu lưu bằng cách states[x]=y, nghĩa là hậu ở hàng x và được lưu ở cột y
# trong đó, states là một list gồm các phần tử
# Hậu lưu bằng cách states[x] = y
# nghĩa là: hậu ở hàng x, cột y
class DuongDi:
    def __init__(self):
        self.states = []
        self.index = 0

    def cap_nhat_states(self, states):
        self.states = states
        self.index = 0

    def next_state(self):
        """Trả về trạng thái kế tiếp hoặc None nếu hết"""
        if self.index < len(self.states):
            state = self.states[self.index]
            self.index += 1
            return state
        return None

    def get_final_state(self):
        """Trả về trạng thái cuối cùng (lời giải)"""
        if self.states:
            return self.states[-1]
        return None
