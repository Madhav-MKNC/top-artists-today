# -*- coding: utf-8 -*-
"""
Fetches the data from kworb.net and presents the stats of most streamed music artists on youtube today by their total view count for the day
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json


def main():
  base_url = "https://kworb.net/youtube/"

  index = "https://kworb.net/youtube/archive.html"
  response = requests.get(index)

  if response.status_code != 200:
    print("[error] status_code:", response.status_code)
    exit()

  soup = BeautifulSoup(response.text, 'html.parser')
  tbody = soup.find('tbody')
  artist_links = tbody.find_all('a',
                                href=lambda x: x and x.startswith('artist/'))

  top_artists_urls = [urljoin(base_url, link['href']) for link in artist_links]
  print("[+] Total top artists:", len(top_artists_urls))

  # get currect daily average views of the artist
  def current_daily_average(artist_url):
    response = requests.get(artist_url)

    try:
      soup = BeautifulSoup(response.text, 'html.parser')
      current_daily_avg_td = soup.find('td')
      # current_daily_avg_td = soup.find('td', text="Current daily avg:")

      if current_daily_avg_td:
        value = current_daily_avg_td.find_next('td').find_next('td').find_next(
            'td').text
        print('loading')
        return float(value.replace(',', '_'))
    except Exception as e:
      print("[error]", artist_url, "=", str(e))

    # failed to fetch page
    print("[error]", artist_url)
    return 0

  # main
  stats = {}

  try:
    for artist_url in top_artists_urls:
      stats[artist_url] = current_daily_average(artist_url)
  except KeyboardInterrupt:
    print("[stopping]")

  print("[***] Ranking the artists...\n")
  sorted_stats = dict(
      sorted(stats.items(), key=lambda item: item[1], reverse=True))

  # persist data
  with open('stats.txt', 'w', encoding='utf-8') as file:
    file.write(json.dumps(sorted_stats))

  rankings = ""
  for rank, artist in enumerate(sorted_stats):
    x = f"[{rank+1}] {sorted_stats[artist]} : {artist.split('/')[-1].split('.')[0]}"
    print(x)
    rankings += x + "\n"

  # persist rankings
  with open('rankings.txt', 'w', encoding='utf-8') as file:
    file.write(rankings)


# api
from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)


@app.route("/")
def home():
  with open("rankings.txt", 'r') as file:
    file_content = file.read()
  print("[+] OK")
  return render_template('file.html', content=file_content)


@app.route("/refresh")
def refresh():
  Thread(target=main).start()
  print("[*] Refreshing...")
  return "Will be refreshed soon"


@app.route("/keep_alive")
def keep_alive():
  print("[+] ping by uptimerobot")
  return "online"


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
