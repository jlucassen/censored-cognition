import json

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
    
    @classmethod
    def from_json(self, path: str):
        with open(path, "r") as f:
            lines = [json.loads(line) for line in f.readlines()]
            return [SolverResult(**solver_result) for solver_result in lines]
        
    @classmethod
    def to_json(self, solver_results: list, path: str):
        with open(path, "w") as f:
            for solver_result in solver_results:
                f.write((solver_result.__repr__() + "\n").replace("'", '"'))
    

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
    
    @classmethod
    def from_json(self, path: str):
        with open(path, "r") as f:
            lines = [json.loads(line) for line in f.readlines()]
            return [JudgeResult(**judge_result) for judge_result in lines]
        
    @classmethod
    def to_json(self, judge_results: list, path: str):
        with open(path, "w") as f:
            for judge_result in judge_results:
                temp = judge_result.correct
                judge_result.correct = str(judge_result.correct)
                f.write((judge_result.__repr__() + "\n").replace("'", '"'))
                judge_result.correct = temp