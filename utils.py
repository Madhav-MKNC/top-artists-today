# -*- coding: utf-8 -*-

from utils import main

from time import time

from flask import Flask, render_template, url_for, jsonify
from threading import Thread
"""
Flask App for hosting API
"""
app = Flask(__name__)
previous_ping = time()


@app.route("/")
def home():
  with open("rankings.txt", 'r') as file:
    file_content = file.read()
  print("[+] OK")
  return render_template('file.html', content=file_content)


# keep alive ping point for uptimerobot as well updates the stats twice an hour
@app.route("/refresh")
def keep_alive():
  global previous_ping
  if time(
  ) - previous_ping > 2000:  # interval of 2000 seconds (approximately half an hour)
    Thread(target=main).start()
    print("[*] Updating...")
  print("[+] ping by uptimerobot")
  return jsonify({"Status": "Updating..."})


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
