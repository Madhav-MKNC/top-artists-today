# -*- coding: utf-8 -*-
"""
Fetches the data from kworb.net and presents the stats of most streamed music artists on youtube today by their total view count for the day
"""

import os
from time import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed


# beautify the numbers (1333333 => 1,333,333)
def bootyfy(num):
    if len(str(num)) < 4:
        return num

    rnum = str(num)[::-1]
    ret = ""
    while True:
        if len(rnum) < 4:
            ret += rnum
            break
        ret += rnum[0:3] + ","
        rnum = rnum[3:]

    return ret[::-1]


counter = 0

# get current daily average views on the artist
def current_daily_average(artist_url):
    global counter
    counter += 1

    response = requests.get(artist_url)

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        current_daily_avg_td = soup.find('td')
        if current_daily_avg_td:
            value = current_daily_avg_td.find_next('td').find_next('td').find_next('td').text
            print(f'[{counter}] Loading {value}')
            return int(float(value.replace(',', '_')))
    except Exception as e:
        print("[error]", artist_url, "=", str(e))

    # failed to fetch page
    print("[error]", artist_url)
    return 0


# main
def main():
    base_url = "https://kworb.net/youtube/"

    index = "https://kworb.net/youtube/archive.html"
    response = requests.get(index)

    if response.status_code != 200:
        print("[error] status_code:", response.status_code)
        exit()

    soup = BeautifulSoup(response.text, 'html.parser')
    tbody = soup.find('tbody')
    artist_links = tbody.find_all('a', href=lambda x: x and x.startswith('artist/'))

    top_artists_urls = [urljoin(base_url, link['href'])
                        for link in artist_links]
    print("[+] Total top artists:", len(top_artists_urls))

    # Multithreading to fetch data concurrently
    stats = {}
    # Adjust the max_workers based on your system
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(
            current_daily_average, url): url for url in top_artists_urls}
        for future in as_completed(future_to_url):
            artist_url = future_to_url[future]
            try:
                stats[artist_url] = future.result()
            except Exception as exc:
                print(f'[error] {artist_url} generated an exception: {exc}')

    print("[***] Ranking the artists...\n")
    sorted_stats = dict(
        sorted(stats.items(), key=lambda item: item[1], reverse=True))

    # persist
    with open('stats.txt', 'w', encoding='utf-8') as file:
        file.write(json.dumps(sorted_stats))

    rankings = ""
    for rank, artist in enumerate(sorted_stats):
        x = f"{rank+1} : {bootyfy(int(float(sorted_stats[artist])))} : {artist.split('/')[-1].split('.')[0]} : {artist}"
        print(x)
        rankings += x + "\n"

    # persist rankings
    with open('rankings.txt', 'w', encoding='utf-8') as file:
        file.write(rankings)


"""
Previous Timestamp
"""
PREVIOUS_FILE_PATH = '.previous_ts'


# set the previous ping timestamp
def set_previous(ts):
    with open(PREVIOUS_FILE_PATH, 'w', encoding='utf-8') as file:
        file.write(str(ts))


# read previous ping timestamp
def get_previous():
    if not os.path.exists(PREVIOUS_FILE_PATH):
        ts = time()
        set_previous(ts)

    with open(PREVIOUS_FILE_PATH, 'r', encoding='utf-8') as file:
        ts = file.read().strip()

    if not ts:
        ts = time()
        set_previous(ts)

    return float(ts)
