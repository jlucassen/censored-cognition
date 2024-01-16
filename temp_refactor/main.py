from sample import Sample
from solver import Solver

samples = Sample.from_json('samples/multiplication_2_2_42.jsonl')
mySolver = Solver('gpt-4')
results = mySolver.solve(samples)