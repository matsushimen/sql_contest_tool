from src.init_problem import InitProblem
import pandas as pd
import lxml
import sys

sys.path.append('.')


class InitContest:

    _base_url = "https://topsic-contest.jp/contests/"

    def __init__(self, contest_name) -> None:
        self._contest_name = contest_name
        self._contest_url = self._base_url + contest_name + '/problems'

    def _get_problem_code_list(self):
        contest_df = pd.read_html(self._contest_url)
        return contest_df[0]['問題コード'].to_list()

    def _init_problem(self, problem_code):
        InitProblem(contest_name=self._contest_name,
                    problem_code=problem_code).run()

    def run(self):
        problem_code_list = self._get_problem_code_list()
        for problem_code in problem_code_list:
            self._init_problem(problem_code=problem_code)
