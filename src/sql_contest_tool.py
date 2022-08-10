import argparse
import sys
sys.path.append('.')
from src.init_contest import InitContest
from src.init_problem import InitProblem

def _init_problem(args):
    InitProblem(contest_name=args.contest_name,
                problem_code=args.problem_code).run()


def _init_contest(args):
    InitContest(contest_name=args.contest_name).run()


def parse_argments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="sub-command help")

    init_problem = subparsers.add_parser("init-problem", aliases=['ip'])
    init_problem.add_argument(
        "--contest_name", "-c", help="https://topsic-contest.jp/contests/'contest_name'/problem/problem_code")
    init_problem.add_argument(
        "--problem_code", "-p", help="https://topsic-contest.jp/contests/contest_name/problem/'problem_code'")
    init_problem.set_defaults(handler=_init_problem)

    init_contest = subparsers.add_parser("init-contest", aliases=['ic'])
    init_contest.add_argument(
        "--contest_name", "-c", help="https://topsic-contest.jp/contests/'contest_name'")
    init_contest.set_defaults(handler=_init_contest)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_argments()
    if hasattr(args, 'handler'):
        args.handler(args)
