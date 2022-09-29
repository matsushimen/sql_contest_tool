import pandas as pd
import lxml
import sqlite3
from urllib import parse, request
from bs4 import BeautifulSoup
from functools import reduce
import os
import sys
sys.path.append('.')
import src.util.util as util

class InitProblem:
    
    _type_dict = {
        "VARCHAR": str,
        "INTEGER": "Int64",
        "FLOAT": float,
        "IMMIGRATION": str  # FIXME hard coding for typo in contest001-3
    }
    _base_url = "https://topsic-contest.jp/contests/"
    
    def __init__(self, contest_name, problem_code) -> None:
        self._contest_name = contest_name
        self._problem_code = problem_code
        self._base_dir = os.path.abspath(os.path.dirname(__file__) + "/../")
        self._db_path = os.path.join(self._base_dir, "contests",
                           self._contest_name, self._problem_code + ".db")
        self._url = reduce(lambda x, y: parse.urljoin(x, y), [
                 self._base_url + "/", self._contest_name + "/", "problems/", self._problem_code])
    
    def _get_table_names(self, soup):
        table_def_start_index = [
            x.string for x in soup.select("h3 , h4")].index('テーブル定義')
        sample_data_start_index = [
            x.string for x in soup.select("h3 , h4")].index('サンプルデータ')
        # TODO ここにvalidate欲しい
        table_names = [x.string.split(": ")[-1] for x in soup.select(
            "h3 , h4")][table_def_start_index+1:sample_data_start_index]
        return table_names


    def _get_table_def(self, soup):
        table_def_start_index = [x.string for x in soup.select(
            "h3 , h4, table")].index('テーブル定義')
        sample_data_start_index = [x.string for x in soup.select(
            "h3 , h4, table")].index('サンプルデータ')
        # TODO ここにvalidate欲しい
        table_def_dfs = pd.read_html("".join([str(x) for x in soup.select(
            "h3 , h4, table")][table_def_start_index+1:sample_data_start_index]))
        table_def_list = []
        for df in table_def_dfs:
            df['dummy'] = 1
            table_def_list.append(df.pivot(index='dummy', columns='列名', values='データ型').replace(
                self._type_dict).reset_index().drop(columns=['dummy']).to_dict(orient='records')[0])

        return table_def_list


    def _create_table(self, soup, conn, table_def_list, table_name_list):

        columns = reduce(lambda x, y: list(x) + list(y),
                        [x.keys() for x in table_def_list])
        converters = {x: str for x in set(columns)}
        sample_data_start_index = [x.string for x in soup.select(
            "h3 , h4, table")].index('サンプルデータ')
        table_dfs = pd.read_html("".join([str(x) for x in soup.select(
            "h3 , h4, table")][sample_data_start_index:]), converters=converters)
        for i in range(len(table_def_list)):
            table_dfs[i].astype(table_def_list[i]).to_sql(
                table_name_list[i], conn, if_exists='replace', index=None)
            
    def _create_db(self):
        conn = sqlite3.connect(self._db_path)
        return conn
        
    def _create_contest_dir(self):
        os.makedirs("contests/" + self._contest_name, exist_ok=True)

    def run(self):
        self._create_contest_dir()
        conn = self._create_db()
        soup = util.get_soup(self._url)
        table_name_list = self._get_table_names(soup)
        table_def_list = self._get_table_def(soup)
        self._create_table(soup, conn, table_def_list, table_name_list)
