import configparser
import requests
from bs4 import BeautifulSoup


class Submit:
    _base_url = "https://topsic-contest.jp/contests/"
    _login_url = "https://topsic-contest.jp/users/sign_in"
    _config_path = "./config.ini"

    def __init__(self, contest_name, problem_code, sql_file_path) -> None:
        self._problem_url = self._base_url + contest_name + "/problems/" + problem_code
        self._user_name, self._password = self._load_config()
        self._session = requests.session()
        self._sql_text = self._open_sql_file(sql_file_path)
        
    # TODO 都度ログインではなくsessionを保存したい
    def _load_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config["user"]["user_name"], config["user"]["password"]

    def _open_sql_file(self, sql_file_path):
        with open(sql_file_path, "r") as f:
            sql_text = f.read()
        return sql_text

    def _get_login_csrf_token(self):
        login_page = self._session.get(self._login_url, cookies="")
        html = BeautifulSoup(login_page.text, "html.parser")
        token = html.find(
            'input', attrs={"type": "hidden", "name": "authenticity_token"})["value"]
        return token

    def _get_problem_cookie_csrf_token(self):
        problem_page = self._session.get(self._problem_url, cookies="")
        html = BeautifulSoup(problem_page.text, "html.parser")
        token = html.find("meta", attrs={"name": "csrf-token"})["content"]
        cookie = self._session.get(
            self._problem_url).headers["set-cookie"].split(';')[0]
        return token, cookie

    def _login(self):
        token = self._get_login_csrf_token()
        payload = {
            "user[login]": self._user_name,
            "user[password]": self._password,
            "authenticity_token": token,
        }
        return self._session.post(self._login_url,
                           data=payload
                           )
        

    def _submit(self, sql_text: str):
        token, cookie = self._get_problem_cookie_csrf_token()
        header = {
            "cookie": cookie,
            "referer": self._problem_url,
            "x-csrf-token": token,
            "x-requested-with": "XMLHttpRequest",
        }
        submit_url = self._problem_url + "/submit"
        payload = {
            "submission[answer]": sql_text,
        }
        submit = self._session.post(submit_url,
                                    headers=header,
                                    data=payload)
        return submit

    def run(self):
        login = self._login()
        if(login.status_code == 200):
            print("Login is Successful")
        else:
            print("Login is Failed")
            exit(1)
        submit = self._submit(self._sql_text)
        if((submit.status_code == 200) & (submit.request.method == "POST")):
            print("Submission is Successful")
        else:
            print("Submission is Failed")
            exit(1)

