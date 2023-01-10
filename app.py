from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import logging
import pandas as pd

logging.getLogger().setLevel(logging.INFO)

external_stylesheets = [dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME]

# Make the dataframe a global variable
global df

# import the dataframe json file
df = pd.read_json('episode2.json')

# Replace weird Unicode formatting with the actual ampersand
df['Name'] = df['Name'].replace('&amp;', '&', regex=True)

app = Dash(
  __name__, 
  external_stylesheets=external_stylesheets,
  # Add meta tags for mobile devices
  # https://community.plotly.com/t/reorder-website-for-mobile-view/33669/5?
  meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
  ],
)

# Set the page title
app.title = "Xenosaga Enemies"
app.description = "A filterable and searchable table of all enemies in the Xenosaga series."

# For Gunicorn
server = app.server

# Plausible privacy-friendly analytics
# https://dash.plotly.com/external-resources#usage (Option 1)
# Probably won't get past adblockers and NoScript but whatever, good enough
app.index_string = """<!DOCTYPE html>
<html>
  <head>
    <script defer data-domain="xenosaga.automateordie.io" src="https://plausible.automateordie.io/js/plausible.js" type="application/javascript"></script>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
  </head>
  <body>
    {%app_entry%}
    <footer>
      {%config%}
      {%scripts%}
      {%renderer%}
    </footer>
  </body>
</html>
"""

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

# Add the DataTable to the app layout

title_card = dbc.Card(
  [
    html.H3("Xenosaga: Enemy List", className="card-title"),
    html.P("A searchable list of enemies in the Xenosaga series."),
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

app.layout = dbc.Container([
  dbc.Row( # First row: title card
    [
      dbc.Col([title_card], lg = 2, md = 4, sm = 6, xs = 8),
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

# Run the app
app.run_server(debug=True)