import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

years = list(range(1991, 2022))
team_stats_url = "https://www.basketball-reference.com/leagues/NBA_{}_standings.html"

"""GET TEAM STATS"""
for year in years:
    time.sleep(10)
    url = team_stats_url.format(year)

    data = requests.get(url)

    with open("team/{}.html".format(year), "w+", encoding="utf-8") as f:
        f.write(data.text)

"""PARSE TEAM STATS"""
dfs = []
for year in years:
    with open("team/{}.html".format(year), encoding="utf-8") as f:
        page = f.read()

    """EASTERN CONFERENCE STANDINGS"""
    soup = BeautifulSoup(page, "html.parser")
    for thead in soup.find_all('tr', class_='thead'):
        thead.decompose()

    team_table = soup.find(id="divs_standings_E")
    team = pd.read_html(StringIO(str(team_table)))[0]
    team["Year"] = year
    team["Team"] = team["Eastern Conference"]
    del team["Eastern Conference"]
    dfs.append(team)

    """WESTERN CONFERENCE STANDINGS"""
    soup = BeautifulSoup(page, "html.parser")
    for thead in soup.find_all('tr', class_='thead'):
        thead.decompose()

    team_table = soup.find(id="divs_standings_W")
    team = pd.read_html(StringIO(str(team_table)))[0]
    team["Year"] = year
    team["Team"] = team["Western Conference"]
    del team["Western Conference"]
    dfs.append(team)

teams = pd.concat(dfs)
teams.to_csv("teams.csv")