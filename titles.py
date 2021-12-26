#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import requests
import time, json, os
from urllib.parse import quote

os.chdir(os.path.dirname(os.path.abspath(__file__)))

BOT_NAME = os.environ["BOT_NAME"]
BOT_PASS = os.environ["BOT_PASS"]
API_ADDRESS = os.environ["API_ADDRESS"]

session = requests.Session()

def Save(titles):
  with open("titles.txt", "w", -1, "utf-8") as f:
    f.write("\t".join(["id", "name", "url"]) + "\n")
    f.write("\n".join([f"{i}\t{i}\thttps://zh.moegirl.org/{quote(i)}" for i in sorted(titles.keys(), key=lambda x: titles[x]["id"], reverse=True)]))

# Login
response = session.post(API_ADDRESS,
  data = {
    "action": "query",
    "meta": "tokens",
    "type": "login"
  })

response = session.post(API_ADDRESS,
  data = {
    "action": "login",
    "lgtoken": response.json()["query"]["tokens"]["logintoken"],
    "lgname": BOT_NAME,
    "lgpassword": BOT_PASS
  })
print("Logged in.")
time.sleep(10)

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
json = response.json()
titles = {}
for page in json["query"]["allpages"]:
  titles[page["title"]] = {
    "id": page["pageid"],
    "title": page["title"]
  }
Save(titles)
print(f"Titles: {len(titles)}")
time.sleep(8)

while "continue" in json and "apcontinue" in json["continue"]:
  kw.update({
    "apcontinue": json["continue"]["apcontinue"]
  })
  response = session.post(API_ADDRESS, data = kw)
  json = response.json()
  for page in json["query"]["allpages"]:
    titles[page["title"]] = {
      "id": page["pageid"],
      "title": page["title"]
    }
  Save(titles)
  print(f"Titles: {len(titles)}")
  time.sleep(8)