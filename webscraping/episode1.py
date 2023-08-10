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
        'EXP': exp,
        'TP': tp,
        'EP': ep,
        'SP': sp,
        'Cash': cash,
        'Normal Drop': item,
        'Rare Drop': rare,
        'Type': type,
        'Weakness': weaknesses,
        
    }
)

# Replace weird Unicode formatting with the actual ampersand
df['Name'] = df['Name'].replace('&amp;', '&', regex=True)

# Replace the string None with N/A
df = df.replace('None', 'N/A')

# Replace empty strings with N/A
df = df.replace('', 'N/A')

# Replace NaN with N/A
df = df.replace(float('nan'), 'N/A')

# Remove all text after '200' in Minitia's SP column
df['SP'] = df['SP'].str.replace(r'200.*', '200', regex=True)

# At this point I had to export the dataframe as a CSV, edit it in Excel to split some of the bosses and their minions into separate rows, and then import it back into Python
# Kind of a pain in the ass

# Convert non-numeric entries to their average or single integer value
def convert_to_avg(x):
    if isinstance(x, str) and '-' in x:
        low, high = x.split('-')
        return (int(low) + int(high)) // 2  # Calculate the average
    else:
        return int(x)

# Cast as nullable integers
numeric_cols = ['HP', 'EXP', 'EP', 'SP', 'Cash', 'TP']
for col in numeric_cols:
    df[col] = df[col].apply(convert_to_avg)
    df[col] = df[col].astype('Int64')  # Cast to nullable integer

# Cast name as string dtype
string_cols = ['Name', 'Normal Drop', 'Rare Drop', 'Type', 'Weakness']
for col in string_cols:
    df[col] = df[col].astype(pd.StringDtype())

# Sort the dataframe alphabetically by Name
df.sort_values(by=['Name'], inplace=True)

# Export to JSON
df.to_json('json/episode1.json')