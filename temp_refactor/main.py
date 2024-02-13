# %%

from sample import Sample
from solver import Solver
from judge import ContainsJudge

# %%
samples = Sample.from_json('samples/multiplication_2_2_42.jsonl')
mySolver = Solver('gpt-4')
myJudge = ContainsJudge()
results = mySolver.solve_samples(samples, myJudge)


# %%
print(len(results))

# %%
print(sum([result.correct for result in results]))
# %%
