class Judge:
    def init(self):
        pass

    def bool_judge(self, sample, response) -> bool:
        raise NotImplementedError

    def num_judge(self, sample, response):
        raise NotImplementedError
    
class ContainsJudge(Judge):
    def bool_judge(self, sample, response):
        return sample.correct_answer in response