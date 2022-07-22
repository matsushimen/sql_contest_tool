import pandas as pd
import lxml
import sqlite3
import sys
from urllib import parse
from functools import reduce

type_dict = {
    "VARCHAR": str,
    "INTEGER": int,
    "FLOAT": float
}

if __name__ == "__main__":
    db = sys.argv[1]
    base_url = "https://topsic-contest.jp/contests/"
    contest_name = sys.argv[2]
    problem_name = sys.argv[3]
    url = reduce(lambda x, y:parse.urljoin(x, y), [base_url + "/", contest_name + "/", "problems/", problem_name])
    #"https://topsic-contest.jp/contests/contest001/problems/contest001-2"
    print(url)
    dfs = pd.read_html(url)
    conn = sqlite3.connect(db)
    for i in range(len(dfs)):
        print("-----------------------------------------------------")
        print(f"table number: {i}")
        print(dfs[i].head())
        ans = input("create this table? Y/n: ")
        if(ans in ["Y", "yes", "y"]):
            table_name = input("Input this table's name: ")
            dfs[i].to_sql(table_name,conn, if_exists='replace',index=None)
            print(f"Created table: {table_name} to {db}")
