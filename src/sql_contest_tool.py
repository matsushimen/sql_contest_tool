import argparse
import sys

sys.path.append('.')
from src.init_problem import InitProblem

def func_init_problem(args):
    InitProblem(contest_name=args.contest_name, problem_name=args.problem_name).init_problem()
    
def parse_argments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="sub-command help")
    
    init_problem = subparsers.add_parser("init-problem", aliases=['ip'])
    init_problem.add_argument("--contest_name", "-c", help="https://topsic-contest.jp/contests/'contest_name'/problem/problem_name")
    init_problem.add_argument("--problem_name", "-p", help="https://topsic-contest.jp/contests/contest_name/problem/'problem_name'")
    init_problem.set_defaults(handler=func_init_problem)
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_argments()
    if hasattr(args, 'handler'):
        args.handler(args)