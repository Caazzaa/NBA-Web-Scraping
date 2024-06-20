import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

years = list(range(1991, 2022))
url_start = "https://www.basketball-reference.com/awards/awards_{}.html"

"""GET MVPS"""
for year in years:
    url = url_start.format(year)
    data = requests.get(url)

    with open("mvp/{}.html".format(year), "w+", encoding="utf-8") as f:
        f.write(data.text)

"""PARSE MVPS"""
dfs = []
for year in years:
    with open("mvp/{}.html".format(year), encoding="utf-8") as f:
        page = f.read()
    soup = BeautifulSoup(page, "html.parser")

    over_header = soup.find('tr', class_="over_header")
    if over_header:
        over_header.decompose()

    mvp_table = soup.find(id="mvp")
    mvp = pd.read_html(StringIO(str(mvp_table)))[0]
    mvp["Year"] = year

    dfs.append(mvp)

mvps = pd.concat(dfs)
mvps.to_csv("mvps.csv")