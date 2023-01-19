from bs4 import BeautifulSoup as bs4
import requests
import re
import pandas as pd

df = pd.read_csv('xenosaga episode 2.csv')

# Convert the strings in the Name column to lowercase except for the first letter
df['Name'] = df['Name'].str.title()

# Strip whitespace from the beginning and end of the strings in all columns
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Insert thousands separators into the numbers
df['HP'] = df['HP'].str.replace(r'(\d)(?=(\d\d\d)+(?!\d))', r'\1,', regex=True)
df['EXP'] = df['EXP'].str.replace(r'(\d)(?=(\d\d\d)+(?!\d))', r'\1,', regex=True)
df['CPTS'] = df['CPTS'].str.replace(r'(\d)(?=(\d\d\d)+(?!\d))', r'\1,', regex=True)
df['SP'] = df['SP'].str.replace(r'(\d)(?=(\d\d\d)+(?!\d))', r'\1,', regex=True)

# Replace the string None with N/A
df = df.replace('None', 'N/A')

# Replace empty strings with N/A
df = df.replace('', 'N/A')

# Replace NaN with N/A
df = df.replace(float('nan'), 'N/A')

# Export dataframe to JSON
df.to_json('webscraping/episode3.json', orient='records')
