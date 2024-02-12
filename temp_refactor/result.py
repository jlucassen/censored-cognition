from sample import Sample

class Result:
    def __init__(
            self,
            sample: Sample,
            response: str,
            correct: bool
    ):
        self.sample = sample
        self.response = response
        self.correct = correct

    def __repr__(self):
        return str(self.__dict__)