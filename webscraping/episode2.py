import pandas as pd

# Read the CSV file into a dataframe
# This is a CSV file I manually created by copying and pasting the enemy data from the Xenosaga Episode II enemy list
df = pd.read_csv('xenosaga episode 2.csv')

# Convert the strings in the Name column to lowercase except for the first letter
df['Name'] = df['Name'].str.title()

# Strip whitespace from the beginning and end of the strings in all columns
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Create a list of columns to convert to numeric
stat_cols = [
  "HP",
  "EXP",
  "CPTS",
  "SPTS",
]

# Convert the columns to nullable integers
for col in stat_cols:
  df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

# Replace the string None with N/A
df = df.replace('None', 'N/A')

# Replace empty strings with N/A
df = df.replace('', 'N/A')

# Convert numbers into percentages for the following columns
weakness_cols = [
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

for col in weakness_cols:
    df[col] = df[col].astype(str) + '%'

# Export dataframe to JSON
df.to_json('json/episode2.json', orient='records')
