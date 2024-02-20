import json

from sample import Sample
from solver import Solver, GPT_3_STRING
from result import SolverResult, JudgeResult
from judge import EQUALS_JUDGE

# make a sample from constructor
my_sample = Sample(0,
                   [{"role": "system", "content": "Repeat what the user says back to them.",},
                    {"role": "user", "content": "Repeat this back!"}],
                    ['censor', 'these', 'strings'],
                    'Repeat this back!')
# save to jsonl and load it back
Sample.to_json([my_sample], 'testfiles/test_sample.jsonl')
my_sample2 = Sample.from_json('testfiles/test_sample.jsonl')[0]
# assert that the two samples are the same
assert my_sample == my_sample2

# make a solver from constructor
my_solver = Solver(GPT_3_STRING, {})
# solve the sample
my_solver_result = my_solver.solve_sample(my_sample)
# save the SolverResult to jsonl and load it back
SolverResult.to_json([my_solver_result], 'testfiles/test_solver_result.jsonl')
my_solver_result2 = SolverResult.from_json('testfiles/test_solver_result.jsonl')[0]
# assert that response is the same
assert my_solver_result.response == my_solver_result2.response
# assert that serializable solver properties are the same
assert my_solver_result.solver.model == my_solver_result2.solver['model']
assert my_solver_result.solver.completion_args == my_solver_result2.solver['completion_args']

# load a judge from const
my_judge = EQUALS_JUDGE
# judge the solver result
my_judge_result = my_judge.judge_solver_result(my_solver_result)
# this task should be easily doable
assert my_judge_result.correct
# save the JudgeResult to jsonl and load it back
JudgeResult.to_json([my_judge_result], 'testfiles/test_judge_result.jsonl')
my_judge_result2 = JudgeResult.from_json('testfiles/test_judge_result.jsonl')[0]
# assert that the judge result is the same
assert my_judge_result2.correct
# assert that serializable judge properties are the same
assert my_judge_result.judge.id == my_judge_result2.judge['id']
assert my_judge_result.judge.judge_function.__name__ == my_judge_result2.judge['judge_function_name']

print("Tests passed!")