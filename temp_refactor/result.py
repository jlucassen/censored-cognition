from sample import Sample

class Result:
    def __init__(
            self,
            sample: Sample,
            response: str,
            correct: bool,
            time: int
    ):
        self.sample = sample
        self.response = response
        self.correct = correct
        self.time = time

    def __repr__(self):
        return str(self.__dict__)