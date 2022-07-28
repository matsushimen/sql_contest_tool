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
    base_url = "https://topsic-contest.jp/contests/"
    contest_name = sys.argv[1]
    problem_name = sys.argv[2]
    db = contest_name + problem_name + ".db"
    url = reduce(lambda x, y:parse.urljoin(x, y), [base_url + "/", contest_name + "/", "problems/", problem_name])
    
    print(url)
    first_dfs = pd.read_html(url)
    conn = sqlite3.connect(db)
    tbl_id_list = []
    tbl_def_id_list = []
    converter_column_list = []
    tbl_name_list = []
    for i in range(len(first_dfs)):
        print("-----------------------------------------------------")
        print(f"table number: {i}")
        print(first_dfs[i].head())
        ans = input("Create this table? Y/n: ")
        if(ans in ["Y", "yes", "y"]):
            """
            ここでは書き込むテーブルと型定義をしているテーブルのインデックスを取るだけにする
            """
            table_name = input("Input this table's name: ")
            tbl_name_list.append(table_name)
            table_def_table_num = input("Choose this table's definition table: ")
            tbl_id_list.append(i)
            tbl_def_id_list.append(int(table_def_table_num))
            converter_column_list.extend(first_dfs[i].columns.to_list())
    converters = {x: str for x in set(converter_column_list)}
    print(f"Creating tables")
    second_dfs = pd.read_html(url, converters=converters)

    for i in range(len(tbl_id_list)):
        print("table_name: ", tbl_name_list[i])
        tmp_df = second_dfs[tbl_def_id_list[i]]
        tmp_df['dummy'] = 1
        table_def = tmp_df.pivot(index='dummy',columns='列名',values='データ型').replace(type_dict).reset_index().drop(columns=['dummy']).to_dict(orient='records')[0]
        
        second_dfs[tbl_id_list[i]].astype(table_def).to_sql(tbl_name_list[i],conn, if_exists='replace',index=None)
        print(f"Created table: {table_name} to {db}")
