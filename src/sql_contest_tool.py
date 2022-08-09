import argparse
import sys

sys.path.append('.')
from src.create_db_from_problem import CreateDbFromProblem

def func_create_db_from_problem(args):
    CreateDbFromProblem(contest_name=args.contest_name, problem_name=args.problem_name).create_db_from_problem()
    
def parse_argments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="sub-command help")
    
    init_problem = subparsers.add_parser("init-problem", aliases=['ip'])
    init_problem.add_argument("--contest_name", "-c", help="https://topsic-contest.jp/contests/'contest_name'/problem/problem_name")
    init_problem.add_argument("--problem_name", "-p", help="https://topsic-contest.jp/contests/contest_name/problem/'problem_name'")
    init_problem.set_defaults(handler=func_create_db_from_problem)
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_argments()
    if hasattr(args, 'handler'):
        args.handler(args)