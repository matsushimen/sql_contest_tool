from urllib import parse, request
from bs4 import BeautifulSoup, Tag
import requests


def get_soup(url):
    req = request.Request(url=url)
    response = request.urlopen(req)
    soup = BeautifulSoup(response, features="html.parser")
    return soup

def _get_login_csrf_token(session: requests.Session, login_url: str):
        login_page = session.get(login_url, cookies="")
        html = BeautifulSoup(login_page.text, "html.parser")
        token = html.find(
            'input', attrs={"type": "hidden", "name": "authenticity_token"})["value"]
        return token

def login(session: requests.Session, login_url:str, user_name: str, password: str):
        token = _get_login_csrf_token(session, login_url)
        payload = {
            "user[login]": user_name,
            "user[password]": password,
            "authenticity_token": token,
        }
        return session.post(login_url,
                           data=payload
                           )