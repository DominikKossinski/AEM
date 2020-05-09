import time

from zad4.solution import Solution


class ILS1(Solution):

    def __init__(self, problem, time):
        super(ILS1, self).__init__(problem)
        self.time = time
        self.set_random()

    def optimize(self):
        start_time = time.time() * 1000
        while True:
            current_time = time.time() * 1000
            if current_time - start_time > self.time:
                break
        print(current_time - start_time)
        self.path = self.build_path(self.nodes)
        self.dist = self.path_distance(self.path)
