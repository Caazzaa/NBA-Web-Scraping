import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

years = list(range(1991, 2022))
player_stats_url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"

"""GET PLAYER STATS"""
service = Service(executable_path="D:/chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

for year in years:   
    url = player_stats_url.format(year)

    driver.get(url)
    driver.execute_script("window.scrollTo(1, 10000)")
    time.sleep(2)

    html = driver.page_source

    with open("player/{}.html".format(year), "w+", encoding="utf-8") as f:
        f.write(html)


"""PARSE PLAYER STATS"""
dfs = []
for year in years:
    with open("player/{}.html".format(year), encoding="utf-8") as f:
        page = f.read()

    soup = BeautifulSoup(page, "html.parser")

    thead = soup.find('tr', class_="thead")
    if thead:
        thead.decompose()

    player_table = soup.find(id="per_game_stats")
    player = pd.read_html(StringIO(str(player_table)))[0]
    player["Year"] = year
    dfs.append(player)

players = pd.concat(dfs)
players.to_csv("players.csv")