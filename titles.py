#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import requests
import time, json, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

BOT_NAME = os.environ["BOT_NAME"]
BOT_PASS = os.environ["BOT_PASS"]
API_ADDRESS = os.environ["API_ADDRESS"]

session = requests.Session()

# Login
response = session.post(API_ADDRESS,
  data = {
    "action": "query",
    "meta": "tokens",
    "type": "login"
  })
time.sleep(5)

response = session.post(API_ADDRESS,
  data = {
    "action": "login",
    "lgtoken": response.json()["query"]["tokens"]["logintoken"],
    "lgname": BOT_NAME,
    "lgpassword": API_ADDRESS
  })
print("Logged in.")
time.sleep(5)

# Get Titles
titles = []

kw = {
  "action": "query",
  "format": "json",
  "list": "allpages",
  "apfilterredir": "nonredirects",
  "aplimit": "max"
}
response = session.post(API_ADDRESS, data = kw)
time.sleep(5)
json = response.json()
titles = [i["title"] for i in json["query"]["allpages"]]
print(f"Titles: {len(titles)}")
with open("titles.txt", "w", -1, "utf-8") as f:
  f.write("\n".join(titles))

while "continue" in json and "apcontinue" in json["continue"]:
  kw.update({
    "apcontinue": json["continue"]["apcontinue"]
  })
  response = session.post(API_ADDRESS, data = kw)
  time.sleep(5)
  json = response.json()
  titles += [i["title"] for i in json["query"]["allpages"]]
  print(f"Titles: {len(titles)}")
  with open("titles.txt", "w", -1, "utf-8") as f:
    f.write("\n".join(titles))