import requests
import aiohttp


def fetch_data(url):
    HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
    data = requests.get(url, headers=HEADERS)
    return data


async def async_fetch_data(url):
    try:
        async with aiohttp.ClientSession() as session:
            HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
            async with session.get(url, headers=HEADERS) as response:
                data = await response.text()
                return data
    except aiohttp.client_exceptions.ServerDisconnectedError:
        return await async_fetch_data(url)