import configparser
import requests
import pandas as pd
from urllib import parse, request
from bs4 import BeautifulSoup, Tag
import lxml
import sys
sys.path.append('.')
import src.util.util as util


class GetContests:
    def __init__(self) -> None:
        self._contests_url = "https://topsic-contest.jp/contests"
        self._soup = util.get_soup(self._contests_url)

    def _get_contest_name_en(self):
        soup = self._soup
        opening_contests_index = [x.string for x in soup.select(
            "h3, a")].index('開催中')
        future_open_contests_index = [x.string for x in soup.select(
            "h3, a")].index('開催予定')
        ended_contests_index = [x.string for x in soup.select(
            "h3, a")].index('終了済')

        opening_contest_names_en = [x['href'].split('/')[2] for x in filter(
            lambda x: x.name == 'a', [x for x in soup.select("h3, a")][opening_contests_index:future_open_contests_index])]
        
        future_contest_names_en = [x['href'].split('/')[2] for x in filter(
            lambda x: x.name == 'a', [x for x in soup.select("h3, a")][future_open_contests_index:ended_contests_index])]

        ended_contest_names_en = [x['href'].split('/')[2] for x in filter(
            lambda x: x.name == 'a', [x for x in soup.select("h3, a")][ended_contests_index:])]

        
        return [opening_contest_names_en, future_contest_names_en, ended_contest_names_en]

    def _show_contests(self):
        contests_dfs = pd.read_html(self._contests_url)
        contest_names_en = self._get_contest_name_en()
        contest_status = ["開催中", "開催予定", "終了済"]
        for contest_num in range(len(contests_dfs)):
            print(contest_status[contest_num])
            if len(contests_dfs[contest_num]) == 0:
                print("なし")
            else:
                contests_dfs[contest_num]['コンテスト英名'] = contest_names_en[contest_num]
                print(contests_dfs[contest_num])
    
    def run(self):
        self._show_contests()
        


if __name__ == "__main__":
    gc = GetContests()
    gc._show_contests()
