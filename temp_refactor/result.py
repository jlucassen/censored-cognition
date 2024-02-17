class SolverResult:
    def __init__(
            self,
            sample,
            solver,
            response: str,
    ):
        self.sample = sample
        self.response = response
        self.solver = solver

    def __repr__(self):
        return str(self.__dict__)
    

class JudgeResult:
    def __init__(
            self,
            sample,
            solver,
            judge,
            response: str,
            correct: bool,
    ):
        self.sample = sample
        self.response = response
        self.solver = solver
        self.judge = judge
        self.correct = correct

    def __repr__(self):
        return str(self.__dict__)