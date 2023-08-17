import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils import fetch_data



URL = "https://www.imdb.com/chart/top/"

page = fetch_data(URL)

soup = BeautifulSoup(page.content, "html.parser")

td = soup.find_all("div",  class_='cli-title')[:10]

links_list = []

for link in td:
    data = link.find_all('a')
    for link in data:
        href = link.get('href')
        full_link = f"https://www.imdb.com{href}"
        links_list.append(full_link)

rank_list = []
title_list = []
rating_list = []

for link in links_list:
    get_data = fetch_data(link)
    soup = BeautifulSoup(get_data.content, "html.parser")
    rank = soup.find('a', class_="top-rated-link").text.split("#")[1]
    title = soup.find('span', class_="fDTGTb").text
    rating = soup.find('span', class_="iZlgcd").text

    if rank and title and rating:
        rank_list.append(rank)
        title_list.append(title)
        rating_list.append(rating)

data = {'Rank': rank_list,
        'Title': title_list,
        'Rating': rating_list}

df = pd.DataFrame(data)
df.to_excel('imdb_movie_data.xlsx', index=False)