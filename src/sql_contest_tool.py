import argparse
import sys
sys.path.append('.')
from src.submit import Submit
from src.init_problem import InitProblem
from src.init_contest import InitContest
from src.get_contests import GetContests

def _init_problem(args):
    InitProblem(contest_name=args.contest_name,
                problem_code=args.problem_code).run()


def _init_contest(args):
    InitContest(contest_name=args.contest_name).run()
    

def _get_contests(args):
    GetContests().run()


def _submit(args):
    Submit(contest_name=args.contest_name,
           problem_code=args.problem_code,
           sql_file_path=args.sql_file_path
           ).run()


def parse_argments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="")

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

    submit = subparsers.add_parser("submit", aliases=['s'])
    submit.add_argument(
        "--contest_name", "-c", help="https://topsic-contest.jp/contests/'contest_name'")
    submit.add_argument(
        "--problem_code", "-p", help="https://topsic-contest.jp/contests/contest_name/problem/'problem_code'")
    submit.add_argument(
        "--sql_file_path", "-f", help="sql file path")
    submit.set_defaults(handler=_submit)
    
    submit = subparsers.add_parser("get-contests", aliases=['gc'])
    submit.set_defaults(handler=_get_contests)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_argments()
    if hasattr(args, 'handler'):
        args.handler(args)
