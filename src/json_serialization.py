import copy
import json

from .judge import (
    Judge,
    JudgeResult,
    contains_digit_judge_func,
    contains_judge_func,
    equals_digit_judge_func,
    equals_judge_func,
)
from .sample import Sample
from .solver import Solver, SolverResult

# This file exists to make custom objects like `Solver` JSON-serializable by implementing our own Encoder and Decoder
# Unfortunately, this is a bit ugly in python, see https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
# Also note that this will not preserve the value of the `logging` helper variable.


class CensoredCognitionJSONEncoder(json.JSONEncoder):
    # This sometimes needs weird defensive programming (like deleting attributes only if they are present for the class)
    # due to the recursive way `json.JSONEncoder` is written (this code is called twice for each custom object)
    def default(self, obj):
        if isinstance(obj, JudgeResult):
            return obj.__dict__ | {"__judge_result__": True}
        if isinstance(obj, Judge):
            return self.remove_unnecessary_attrs(obj.__dict__, ["lock"]) | {
                "__judge__": True
            }
        if isinstance(obj, Sample):
            return obj.__dict__ | {"__sample__": True}
        if isinstance(obj, SolverResult):
            return obj.__dict__ | {"__solver_result__": True}
        if isinstance(obj, Solver):
            return self.remove_unnecessary_attrs(
                obj.__dict__, ["client", "encoding", "lock"]
            ) | {"__solver__": True}
        return super().default(obj)

    def remove_unnecessary_attrs(self, d: dict, attrs_to_remove: list[str]) -> dict:
        result = copy.copy(d)
        for attr_to_remove in attrs_to_remove:
            if attr_to_remove in result:
                del result[attr_to_remove]
        return result


def json_decoding_object_hook(json_obj):
    if "__judge_result__" in json_obj:
        return JudgeResult(
            json_obj["sample"],
            json_obj["solver"],
            json_obj["judge"],
            json_obj["response"],
            json_obj["correct"],
            logging=False,
        )
    if "__judge__" in json_obj:
        return Judge(json_obj["id"], json_obj["judge_function_name"], logging=False)
    if "__sample__" in json_obj:
        return Sample(
            json_obj["id"],
            json_obj["messages"],
            json_obj["censored_strings"],
            json_obj["correct_answer"],
        )
    if "__solver_result__" in json_obj:
        return SolverResult(
            json_obj["sample"], json_obj["solver"], json_obj["response"], logging=False
        )
    if "__solver__" in json_obj:
        return Solver(json_obj["model"], json_obj["completion_args"], logging=False)
    return json_obj


## The following deserialization methods unfortunately have to live here instead of in their classes as we otherwise get circular imports


# Legacy code to (de)serialize SolverResults to/from jsonl files
def deserialize_solver_results_from_json(path: str):
    with open(path, "r") as f:
        return [
            json.loads(line, object_hook=json_decoding_object_hook)
            for line in f.readlines()
        ]


def serialize_solver_results_to_json(solver_results: list, path: str):
    with open(path, "w") as f:
        for solver_result in solver_results:
            f.write(json.dumps(solver_result, cls=CensoredCognitionJSONEncoder) + "\n")


# Legacy code to (de)serialize JudgeResults to/from jsonl files
def deserialize_judge_results_from_json(path: str):
    with open(path, "r") as f:
        return [
            json.loads(line, object_hook=json_decoding_object_hook)
            for line in f.readlines()
        ]


def serialize_judge_results_to_json(judge_results: list, path: str):
    with open(path, "w") as f:
        for judge_result in judge_results:
            temp = judge_result.correct
            judge_result.correct = str(judge_result.correct)
            f.write(json.dumps(judge_result, cls=CensoredCognitionJSONEncoder) + "\n")
            judge_result.correct = temp
