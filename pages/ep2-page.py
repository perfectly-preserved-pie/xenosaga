from dash import dash_table, dash, html
import dash_bootstrap_components as dbc
import logging
import pandas as pd

dash.register_page( # https://dash.plotly.com/urls#dash.register_page
    __name__,
    path='/ep2', # URL path
    title='Xenosaga Episode II: Jenseits von Gut und Böse Enemy Database', # HTML title
    name='Xenosaga Episode II: Jenseits von Gut und Böse Enemy Database', 
    )

logging.getLogger().setLevel(logging.INFO)

external_stylesheets = [dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME]

# Make the dataframe a global variable
global df

# import the dataframe json file
df = pd.read_json('/json/episode2.json')

# Create the Dash DataTable
table = dash_table.DataTable(
    columns=[
        {"name": i, "id": i} for i in df.columns
    ],
    data=df.to_dict("records"),
    tooltip_data=[
        {
            'Name': {'value': f"""
            Name: {row['Name']}
            HP: {row['HP']}
            Weakness: {row['Weakness']}
            EXP: {row['EXP']}
            TP: {row['TP']}
            EP: {row['EP']}
            SP: {row['SP']}
            Rare: {row['Rare']}
            Item: {row['Item']}
            Type: {row['Type']}
            Cash: {row['Cash']}""", 'type': 'markdown'},
            'HP': {'value': f"""
            Name: {row['Name']}
            HP: {row['HP']}
            Weakness: {row['Weakness']}
            EXP: {row['EXP']}
            TP: {row['TP']}
            EP: {row['EP']}
            SP: {row['SP']}
            Rare: {row['Rare']}
            Item: {row['Item']}
            Type: {row['Type']}
            Cash: {row['Cash']}""", 'type': 'markdown'},
            'Weakness': {'value': f"""
            Name: {row['Name']}
            HP: {row['HP']}
            Weakness: {row['Weakness']}
            EXP: {row['EXP']}
            TP: {row['TP']}
            EP: {row['EP']}
            SP: {row['SP']}
            Rare: {row['Rare']}
            Item: {row['Item']}
            Type: {row['Type']}
            Cash: {row['Cash']}""", 'type': 'markdown'},
            'EXP': {'value': f"""
            Name: {row['Name']}
            HP: {row['HP']}
            Weakness: {row['Weakness']}
            EXP: {row['EXP']}
            TP: {row['TP']}
            EP: {row['EP']}
            SP: {row['SP']}
            Rare: {row['Rare']}
            Item: {row['Item']}
            Type: {row['Type']}
            Cash: {row['Cash']}""", 'type': 'markdown'},
            'TP': {'value': f"""
            Name: {row['Name']}
            HP: {row['HP']}
            Weakness: {row['Weakness']}
            EXP: {row['EXP']}
            TP: {row['TP']}
            EP: {row['EP']}
            SP: {row['SP']}
            Rare: {row['Rare']}
            Item: {row['Item']}
            Type: {row['Type']}
            Cash: {row['Cash']}""", 'type': 'markdown'},
            'EP': {'value': f"""
            Name: {row['Name']}
            HP: {row['HP']}
            Weakness: {row['Weakness']}
            EXP: {row['EXP']}
            TP: {row['TP']}
            EP: {row['EP']}
            SP: {row['SP']}
            Rare: {row['Rare']}
            Item: {row['Item']}
            Type: {row['Type']}
            Cash: {row['Cash']}""", 'type': 'markdown'},
            'SP': {'value': f"""
            Name: {row['Name']}
            HP: {row['HP']}
            Weakness: {row['Weakness']}
            EXP: {row['EXP']}
            TP: {row['TP']}
            EP: {row['EP']}
            SP: {row['SP']}
            Rare: {row['Rare']}
            Item: {row['Item']}
            Type: {row['Type']}
            Cash: {row['Cash']}""", 'type': 'markdown'},
            'Rare': {'value': f"""
            Name: {row['Name']}
            HP: {row['HP']}
            Weakness: {row['Weakness']}
            EXP: {row['EXP']}
            TP: {row['TP']}
            EP: {row['EP']}
            SP: {row['SP']}
            Rare: {row['Rare']}
            Item: {row['Item']}
            Type: {row['Type']}
            Cash: {row['Cash']}""", 'type': 'markdown'},
            'Item': {'value': f"""
            Name: {row['Name']}
            HP: {row['HP']}
            Weakness: {row['Weakness']}
            EXP: {row['EXP']}
            TP: {row['TP']}
            EP: {row['EP']}
            SP: {row['SP']}
            Rare: {row['Rare']}
            Item: {row['Item']}
            Type: {row['Type']}
            Cash: {row['Cash']}""", 'type': 'markdown'},
            'Type': {'value': f"""
            Name: {row['Name']}
            HP: {row['HP']}
            Weakness: {row['Weakness']}
            EXP: {row['EXP']}
            TP: {row['TP']}
            EP: {row['EP']}
            SP: {row['SP']}
            Rare: {row['Rare']}
            Item: {row['Item']}
            Type: {row['Type']}
            Cash: {row['Cash']}""", 'type': 'markdown'},
            'Cash': {'value': f"""
            Name: {row['Name']}
            HP: {row['HP']}
            Weakness: {row['Weakness']}
            EXP: {row['EXP']}
            TP: {row['TP']}
            EP: {row['EP']}
            SP: {row['SP']}
            Rare: {row['Rare']}
            Item: {row['Item']}
            Type: {row['Type']}
            Cash: {row['Cash']}""", 'type': 'markdown'}
        } for row in df.to_dict('records')
    ],
    tooltip_delay=0,
    tooltip_duration=None,
    id='datatable-interactivity',
    filter_action="native",
    filter_options={
        'case': 'insensitive',
        'placeholder_text': 'Type a string to search...'
    },
    sort_action="native",
)

page_title_card = dbc.Card(
  [
    html.H3("Xenosaga Episode II: Jenseits von Gut und Böse Enemy Database", className="card-title"),
    html.P("A searchable database of enemies in Xenosaga Episode II."),
    html.P(f"Click on the other tabs to see enemy list for the other games."),
    html.I( # use a GitHub icon for my repo
      className="bi bi-github",
      style = {
        "margin-right": "5px",
        "margin-left": "5px"
      },
    ),
    html.A("GitHub", href='https://github.com/perfectly-preserved-pie/xenosaga', target='_blank'),
    html.I( # Add an icon for my blog
      className="fa-solid fa-blog",
      style = {
        "margin-right": "5px",
        "margin-left": "15px"
      },
    ),
    html.A("About This Project", href='https://automateordie.io/xenosaga/', target='_blank'),
  ],
  body = True
)

layout = dbc.Container([
  dbc.Row( # First row: title card
    [
      dbc.Col([page_title_card], lg = 2, md = 4, sm = 6, xs = 8),
    ]
  ),
  dbc.Row( # Second row: the rest
    [
      # Use column width properties to dynamically resize the cards based on screen size
      # https://community.plotly.com/t/layout-changes-with-screen-size-and-resolution/27530/6
      dbc.Col([table], lg = 10, md = 8, sm = 6, xs = 4),
    ]
  ),
],
fluid = True,
className = "dbc"
)