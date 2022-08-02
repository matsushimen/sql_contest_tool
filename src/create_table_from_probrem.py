import pandas as pd
import lxml
import sqlite3
import sys
from urllib import parse, request
from bs4 import BeautifulSoup
from functools import reduce
import os

type_dict = {
    "VARCHAR": str,
    "INTEGER": int,
    "FLOAT": float,
    "IMMIGRATION": str #FIXME hard coding for typo in contest001-3
}


def get_table_names(soup):
    table_def_start_index = [x.string for x in soup.select("h3 , h4")].index('テーブル定義')
    sample_data_start_index = [x.string for x in soup.select("h3 , h4")].index('サンプルデータ')
    #TODO ここにvalidate欲しい
    table_names = [x.string.split(": ")[-1] for x in soup.select("h3 , h4")][table_def_start_index+1:sample_data_start_index]
    return table_names


def get_table_def(soup):
    table_def_start_index = [x.string for x in soup.select("h3 , h4, table")].index('テーブル定義')
    sample_data_start_index = [x.string for x in soup.select("h3 , h4, table")].index('サンプルデータ')
    #TODO ここにvalidate欲しい
    table_def_dfs = pd.read_html("".join([str(x) for x in soup.select("h3 , h4, table")][table_def_start_index+1:sample_data_start_index]))
    table_def_list = []
    for df in table_def_dfs:
        df['dummy'] = 1
        table_def_list.append(df.pivot(index='dummy',columns='列名',values='データ型').replace(type_dict).reset_index().drop(columns=['dummy']).to_dict(orient='records')[0])

    return table_def_list


def create_table(soup, conn, table_def_list, table_name_list):
    
    columns = reduce(lambda x,y: list(x) +list(y), [x.keys() for x in table_def_list])
    converters = {x: str for x in set(columns)}
    sample_data_start_index = [x.string for x in soup.select("h3 , h4, table")].index('サンプルデータ')
    table_dfs = pd.read_html("".join([str(x) for x in soup.select("h3 , h4, table")][sample_data_start_index:]), converters=converters)
    for i in range(len(table_def_list)):
        table_dfs[i].astype(table_def_list[i]).to_sql(table_name_list[i],conn, if_exists='replace',index=None)


if __name__ == "__main__":
    base_url = "https://topsic-contest.jp/contests/"
    contest_name = sys.argv[1]
    problem_name = sys.argv[2]
    os.makedirs("contests/" + contest_name, exist_ok=True)
    base_dir = os.path.abspath(os.path.dirname(__file__) + "/../")
    db_path = os.path.join(base_dir, "contests", contest_name, problem_name + ".db")
    url = reduce(lambda x, y:parse.urljoin(x, y), [base_url + "/", contest_name + "/", "problems/", problem_name])
    req = request.Request(url=url)
    response = request.urlopen(req)
    soup = BeautifulSoup(response,features="html.parser")
    print("probrem: " + url)
    conn = sqlite3.connect(db_path)
    table_def_list = get_table_def(soup)
    table_name_list = get_table_names(soup)
    
    print("table names : ", ",".join(table_name_list))
    print("table definitions : \n", "\n".join([str(x) for x in table_def_list]))
    create_table(soup, conn, table_def_list, table_name_list)
