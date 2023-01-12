from bs4 import BeautifulSoup as bs4
import requests
import re
import pandas as pd

# Pretend like we're human
# https://stackoverflow.com/a/43441551
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

url = "https://gamefaqs.gamespot.com/ps2/929933-xenosaga-episode-iii-also-sprach-zarathustra/faqs/45192"


response = requests.get(url, headers=headers)
soup = bs4(response.content, "html.parser")

# Find the div/class with the id "faqtext"
text = soup.find_all("div", class_="faqtext", id="faqtext")

# Craft a Python regex to get all numbers and commas after "HP: " but before any number of whitespaces followed by "|"
hp = re.findall(r'HP:\s*([\d,]+)[^|]*', str(text))
# Some of the other stat values are N/A, so we need to use a different regex
# Craft a Python regex to get all text after EXP: but before any number of whitespaces followed by |
exp = re.findall(r'Exp:\s*([^|\s]+)[^|]*', str(text))
ep = re.findall(r'EP:\s*([^|\s]+)[^|]*', str(text))
sp = re.findall(r'SP:\s*([^|\s]+)[^|]*', str(text))
gold = re.findall(r'Gold:\s*([^|\s]+)[^|]*', str(text))
bl = re.findall(r'BL:\s*([^|\s]+)[^|]*', str(text))
# Craft a Python regex to get a single letter after Enemy Type: but before any number of whitespaces followed by |
type = re.findall(r'Enemy Type:([A-Z\s]+)[^|]*', str(text))
