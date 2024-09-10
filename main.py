# -*- coding: utf-8 -*-

from utils import main, get_previous, set_previous

from time import time

from flask import Flask, render_template, url_for, jsonify
from threading import Thread
"""
Flask App for hosting API
"""
app = Flask(__name__)

# previous ping timestamp
previous_ping = get_previous()


@app.route("/")
def home():
  print("[+] OK")

  with open("rankings.txt", 'r', encoding='utf-8') as file:
    file_content = file.read().split('\n')

  artists = []
  for i in file_content:
    try:
      item = i.split(" : ")
      rank = item[0]
      views = item[1]
      name = item[2]
      url = item[3]
      artists.append((rank, views, name, url))

    except Exception as e:
      print(e)
      print(f"'{i}' as {file_content.index(i)+1}th line.")

  return render_template('file.html', artists=artists)


# keep alive ping point for uptimerobot as well updates the stats twice an hour
@app.route("/refresh")
def keep_alive():
  global previous_ping

  current_ping = time()
  print("[?] Ping after:", (current_ping - previous_ping) / 60, "minutes")

  if current_ping - previous_ping > 50:  # 50s
    Thread(target=main).start()
    print(f"[*] Updating after {(current_ping-previous_ping)/60} minutes.")

    # update 'previous_ping'
    previous_ping = current_ping
    set_previous(previous_ping)
    
    return jsonify({"Status": "Updating..."})

  return jsonify({"Status": "Updated"})


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
