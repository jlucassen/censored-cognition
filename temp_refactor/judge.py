from datetime import datetime

from result import SolverResult, JudgeResult

class Judge:
    '''
    Specifies how to judge a solver's response. Includes:
    - an id
    - a judge function, SolverResult -> JudgeResult
    
    Has a function to batch judging function over a list of solver results.
    Has a repr that returns str(self.dict)
    Has some const judges with common judge functions.
    '''
    def __init__(self, id, judge_function:callable):
        self.id = id
        self.judge_function = judge_function

        self.log_filename = datetime.now().strftime('logs/judge_results/judge_result_log_%Y_%m_%d_%H%M%S.txt')
        open(self.log_filename, "w")

    def judge_samples(self, solver_results):
        assert isinstance(solver_results, list) and isinstance(solver_results[0], SolverResult)
        judge_bools = [self.judge_function(solver_result) for solver_result in solver_results]
        judge_results = [JudgeResult(solver_result.sample, solver_result.solver, self, solver_result.response, judge_bool) for solver_result, judge_bool in zip(solver_results, judge_bools)]
        assert all([isinstance(x, JudgeResult) for x in judge_results])
        with open(self.log_filename, 'a') as logfile:
            logfile.write("\n".join([judge_result.__repr__() for judge_result in judge_results]))
        return judge_results
    
    def __repr__(self):
        return str(self.__dict__)
    
CONTAINS_JUDGE = Judge(0, lambda solver_response: str(solver_response.sample.correct_answer) in str(solver_response.response))
EQUALS_JUDGE = Judge(1, lambda solver_response: str(solver_response.sample.correct_answer) == str(solver_response.response))