import pandas as pd

# Import a custom CSV I made for Episode 2
df = pd.read_csv('xenosaga episode 2.csv')

# Convert the strings in the Name column to lowercase except for the first letter
df['Name'] = df['Name'].str.title()

# Strip whitespace from the beginning and end of the strings in all columns
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Cast the numeric columns as nullable integers
cols = ['HP', 'EXP', 'CPTS', 'SPTS', 'STR', 'VIT', 'POWER', 'ARMOR', 'EATK', 'EDEF', 'DEX', 'EVA']
for col in cols:
    try:
        df[col] = df[col].astype('Int64')
    except ValueError:
        print(f"Column '{col}' could not be cast as nullable integer.")

# Replace the string None with N/A
df = df.replace('None', 'N/A')

# Replace empty strings with N/A
df = df.replace('', 'N/A')

#df.fillna('N/A', inplace=True)

# Reset the index
df.reset_index(drop=True, inplace=True)

# Sort the dataframe alphabetically by Name
df.sort_values(by=['Name'], inplace=True)

# Export dataframe to JSON
df.to_json('json/episode2.json', orient='records')
