import requests
from bs4 import BeautifulSoup
import pandas as pd
import asyncio
import aiohttp
from utils import fetch_data, async_fetch_data


URL = "https://www.imdb.com/chart/top/"

page = fetch_data(URL)

soup = BeautifulSoup(page.content, "html.parser")

td = soup.find_all("div",  class_='cli-title')[:50]
print(td,"11111111")

links_list = []

for link in td:
    data = link.find_all("a")
    for link in data:
        href = link.get('href')
        full_link = f"https://www.imdb.com{href}"
        links_list.append(full_link)


async def main():
    tasks = [asyncio.create_task(async_fetch_data(links)) for links in links_list]
    return await asyncio.gather(*tasks)

results = asyncio.run(main())

rank_list = []
title_list = []
rating_list = []


for data in results:
    soup = BeautifulSoup(data, "html.parser")
    rank = soup.find('a', class_="top-rated-link").text.split("#")[1]
    title = soup.find('span', class_="fDTGTb").text
    rating = soup.find('span', class_="iZlgcd").text
    print(title)
    if rank and title and rating:
        rank_list.append(rank)
        title_list.append(title)
        rating_list.append(rating)

data = {'Rank': rank_list,
        'Title': title_list,
        'Rating': rating_list}

df = pd.DataFrame(data)
writer = pd.ExcelWriter('imdb_movie_data.xlsx', engine='xlsxwriter')
df.to_excel(writer, index=False)
workbook = writer.book
worksheet = writer.sheets['Sheet1']
max_col = max([len(i) for i in title_list]) + 1
print(max_col,"89898998989998989")
worksheet.set_column('B:B', max_col)
writer.close()