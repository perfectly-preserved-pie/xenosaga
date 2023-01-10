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

url = "https://gamefaqs.gamespot.com/ps2/519264-xenosaga-episode-i-der-wille-zur-macht/faqs/22927"


response = requests.get(url, headers=headers)
soup = bs4(response.content, "html.parser")

# Find the div/class with the id "faqtext"
text = soup.find_all("div", class_="faqtext", id="faqtext")

# Use regex to extract the names of all the enemies
# This regular expression will match "Name:" followed by one or more whitespace characters, and then one or more characters that are not a carriage return ([^\r]+). 
# The string of characters will be captured and returned as a single match.
names = re.findall(r'Name:\s+([^\r]+)', str(text))
# Get all the HP values
hp = re.findall(r'HP:\s+([^\r]+)', str(text))
# and so on
weaknesses = re.findall(r'Weak:\s+([^\r]+)', str(text))
exp = re.findall(r'EXP:\s+([^\r]+)', str(text))
tp = re.findall(r'TP:\s+([^\r]+)', str(text))
ep = re.findall(r'EP:\s+([^\r]+)', str(text))
sp = re.findall(r'SP:\s+([^\r]+)', str(text))
rare = re.findall(r'Rare:\s+([^\r]+)', str(text))
item = re.findall(r'Item:\s+([^\r]+)', str(text))
type = re.findall(r'Type:\s+([^\r]+)', str(text))
cash = re.findall(r'Cash:\s+([^\r]+)', str(text))

# We got lucky because all of these lists have the exact same number of elements (no mismatches)
# Combine all lists into a dataframe
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

# Replace weird Unicode formatting with the actual ampersand
df['Name'] = df['Name'].replace('&amp;', '&', regex=True)