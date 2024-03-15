import json


class Sample:
    """
    Specifies a task sample. Includes:
    - an id
    - a prompt
    - a list of strings to censor
    - a correct answer

    Has class methods to save to / load from .jsonl files.
    Has a repr that returns str(self.dict)
    Has an eq method that compares the __dict__ of two samples.
    """

    def __init__(
        self,
        id: int,
        messages: list[dict],
        censored_strings=list[str],
        correct_answer=str,
    ):
        self.id = id
        self.messages = messages
        self.censored_strings = censored_strings
        self.correct_answer = correct_answer

    @classmethod
    def from_json(self, path: str):
        with open(path, "r") as f:
            lines = [json.loads(line) for line in f.readlines()]
            return [Sample(**sample) for sample in lines]

    @classmethod
    def to_json(self, samples: list, path: str):
        with open(path, "w") as f:
            for sample in samples:
                print("\n\nSerializing sample:\n")
                print(sample.__dict__)
                f.write(json.dumps(sample.__dict__) + "\n")

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__
