import pandas as pd

# Read the JSON files into dataframes for each episode
ep1_df = pd.read_json('assets/json/episode1.json', lines=True)
ep2_df = pd.read_json('assets/json/episode2.json', lines=True)
ep3_df = pd.read_json('assets/json/episode3.json', lines=True)