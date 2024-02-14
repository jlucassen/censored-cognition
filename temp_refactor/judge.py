class Judge:
    def init(self):
        pass

    def bool_judge(self, sample, response) -> bool:
        raise NotImplementedError

    def num_judge(self, sample, response):
        raise NotImplementedError
    
class ContainsJudge(Judge):
    def bool_judge(self, sample, response):
        return str(sample.correct_answer) in str(response)
    
class EqualsJudge(Judge):
    def bool_judge(self, sample, response):
        return str(sample.correct_answer) == str(response)