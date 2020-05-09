from zad4.solution import Solution


class MSLS(Solution):

    def __init__(self, problem):
        super(MSLS, self).__init__(problem)

    def optimize(self):
        best_solution = None
        best_distance = None
        for i in range(100):
            self.set_random()
            self.run_algorithm()
            if best_distance is None or best_distance > self.dist:
                print("Best")
                best_distance = self.dist
                best_solution = self.path

        self.path = best_solution
        self.dist = best_distance

    def run_algorithm(self):
        
        pass