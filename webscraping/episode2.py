import pandas as pd
import re

df = pd.read_csv('xenosaga episode 2.csv')

# Convert the strings in the Name column to lowercase except for the first letter
df['Name'] = df['Name'].str.title()

# Strip whitespace from the beginning and end of the strings in all columns
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Replace the string None with N/A
df = df.replace('None', 'N/A')

# Replace empty strings with N/A
df = df.replace('', 'N/A')

# Replace NaN with N/A
df = df.replace(float('nan'), 'N/A')

# Convert numbers into percentages for the following columns
cols = [
    'Beam',
    'Aura',
    'Thunder',
    'Fire',
    'Ice',
    'Pierce',
    'Slash',
    'Hit',
    'Slow',
    'Heavy',
    'Weak',
    'EthPD',
    'EthDD',
    'Junk',
    'ResDw',
    'Lost',
    'Curse',
]

for col in cols:
    df[col] = df[col].astype(str) + '%'

# Export dataframe to JSON
df.to_json('json/episode2.json', orient='records')
