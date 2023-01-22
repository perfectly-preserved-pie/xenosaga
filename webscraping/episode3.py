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
# This regex will match any string that starts with "AB: " followed by one or more characters that are not "|" 
ab = re.findall(r'AB:\s([^|]+)', str(text))
# and so on...
wk = re.findall(r'WK:\s([^|]+)', str(text))
sg = re.findall(r'SG:\s([^|]+)', str(text))
ne = re.findall(r'NE:\s([^|]+)', str(text))
# Remove trailing whitespaces from these lists
ab = [x.strip() for x in ab]
wk = [x.strip() for x in wk]
sg = [x.strip() for x in sg]
ne = [x.strip() for x in ne]
# Again, drop the first element because it's empty
del ab[0]
del wk[0]
del sg[0]


# And now, all of our lists have the same length, so we can create a Pandas DataFrame
df = pd.DataFrame(
    {
        'Name': names,
        'HP': hp,
        'EXP': exp,
        'EP': ep,
        'SP': sp,
        'Gold': gold,
        'Break Limit': bl,
        'Normal Drop': item,
        'Rare Drop': rare,
        'Stealable Item': superrare,
        'Type': type,
        'Absorbs Element': ab,
        'Weak to Element': wk,
        'Strong Against Element': sg,
        'Not Affected by Element': ne
    }
)

# Replace missing values with "N/A"
df.replace('', 'N/A', inplace=True)

# Replace enemy type abbreviations with full names
df['Type'] = df['Type'].replace({
    'B': 'Biological',
    'G': 'Gnosis',
    'M': 'Mechanical'
})

# Replace element abbreviations with full names
# Use .filter() to select columns containing 'Element'
cols = df.filter(like='Element').columns
# Create functions to replace the abbreviations with full names
def replace_I(x):
    return str(x).replace('I', 'Ice')
def replace_F(x):
    return str(x).replace('F', 'Fire')
def replace_B(x):
    return str(x).replace('B', 'Beam')
def replace_L(x):
    return str(x).replace('L', 'Lightning')
# Apply the functions to the columns
df[cols] = df[cols].applymap(replace_I)
df[cols] = df[cols].applymap(replace_F)
df[cols] = df[cols].applymap(replace_B)
df[cols] = df[cols].applymap(replace_L)

# Add a space after commas in the selected columns
df[cols] = df[cols].apply(lambda x: x.str.replace(',', ', '))

# Remove the (FINAL BOSS) part of the name of the final boss
df['Name'] = df['Name'].replace({'(FINAL BOSS)Zarathustra': 'Zarathustra'})

# Remove the (Boss) string in the name of the boss enemies
df['Name'] = df['Name'].str.replace('\(Boss\)','', regex=True)

# Export dataframe to JSON
df.to_json('json/episode3.json', orient='records')