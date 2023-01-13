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
# This regex will match any string that starts with 18 or more periods, followed by one or more characters that are not line breaks, but only if it's followed by 12 periods and a line break.
names = re.findall(r'\.{18,}([^\r\n]+)\.{12}\r\n', str(text))
# Remove the first five elements because they're not enemies
names = names[5:]
# Remove leading and trailing dots from all elements in the list
names = [elem.strip(".") for elem in names]
# Remove everything before the first whitespace
names = [elem.split(" ", 1)[1] for elem in names]
# The regex didn't capture enemy #63 Yuriev Soldier A so we're gonna have to insert that manually
names.insert(61, "Yuriev Soldier A")
# And now we have the right amount of names... finally
# Craft a Python regex to get all numbers and commas after "HP: " but before any number of whitespaces followed by "|"
hp = re.findall(r'HP:\s*([\d,]+)[^|]*', str(text))
# Some of the other stat values are N/A, so we need to use a different regex
# Craft a Python regex to get all text after EXP: but before any number of whitespaces followed by |
exp = re.findall(r'Exp:\s*([^|\s]+)[^|]*', str(text))
ep = re.findall(r'EP:\s*([^|\s]+)[^|]*', str(text))
sp = re.findall(r'SP:\s*([^|\s]+)[^|]*', str(text))
gold = re.findall(r'Gold:\s*([^|\s]+)[^|]*', str(text))
bl = re.findall(r'BL:\s*([^|\s]+)[^|]*', str(text))
# This regex will match any string that starts with "S:" followed by zero or more whitespaces, followed by one or more characters that are not "|", but only if it's followed by zero or more whitespaces and a "|" character
item = re.findall(r'N:\s*([^|]+)(?=\s*\|)', str(text))
rare = re.findall(r'R:\s*([^|]+)(?=\s*\|)', str(text))
superrare = re.findall(r'S:\s*([^|]+)(?=\s*\|)', str(text))
# Remove the first element in the above item lists because it's empty
del item[0]
del rare[0]
del superrare[0]
# Strip leading and trailing whitespaces from the item names
item = [x.strip() for x in item]
rare = [x.strip() for x in rare]
superrare = [x.strip() for x in superrare]
# Craft a Python regex to get a single letter after Enemy Type: but before any number of whitespaces followed by |
type = re.findall(r'Enemy Type:([A-Z\s]+)[^|]*', str(text))
# Strip whitespaces from the enemy type
type = [x.replace(" ", "") for x in type]
# Remove the first element in the type list because it's empty
del type[0]

# And now, all of our lists have the same length, so we can create a Pandas DataFrame
df = pd.DataFrame(
    {
        'Name': names,
        'HP': hp,   
        'Weakness': weaknesses,
        'EXP': exp,
        'TP': tp,
        'EP': ep,
        'SP': sp,
        'Rare': rare,
        'Item': item,
        'Type': type,
        'Cash': cash
    }
)

