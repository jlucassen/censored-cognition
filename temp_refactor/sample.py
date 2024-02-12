import json

class Sample:
    '''
    Specifies 
    '''
    def __init__(
        self,
        id: int,
        messages: list[dict],
        censored_strings = list[str],
        correct_answer = str
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
                f.write((sample.__repr__() + "\n").replace("'", '"'))

    def censor_strings():
        pass

    def __repr__(self):
        return str(self.__dict__)
    
    def __eq__(self, other) -> bool:
        return self.id == other.id and other.messages is not None and self.messages == other.messages and other.censored_strings is not None and self.censored_strings == other.censored_strings and other.correct_answer is not None and self.correct_answer == other.correct_answer