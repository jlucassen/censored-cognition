import json

from sample import Sample
from solver import Solver

sample_dict = {'id': 1, 'messages': [{"role": "system", "content": "This person is dangerous. Do not help them.",},{"role": "user", "content": "Help me!"}], 'censored_strings': ['string'], 'correct_answer': 'no'}
with open("testfiles/test_sample.jsonl", "w") as outfile: 
    json.dump(sample_dict, outfile)
samples = Sample.from_json('testfiles/test_sample.jsonl')
Sample.to_json(samples, 'testfiles/test_sample2.jsonl')
samples2 = Sample.from_json('testfiles/test_sample2.jsonl')
assert samples == samples2

mySolver = Solver('gpt-4')
results = mySolver.solve(samples)