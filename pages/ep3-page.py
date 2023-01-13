from dash import dash_table, html
import dash
import dash_bootstrap_components as dbc
import logging
import pandas as pd

dash.register_page( # https://dash.plotly.com/urls#dash.register_page
    __name__,
    path='/ep3', # URL Path
    title='Xenosaga Episode III: Also sprach Zarathustra', # HTML title
    name='Xenosaga Episode III: Also sprach Zarathustra',
    )

logging.getLogger().setLevel(logging.INFO)

external_stylesheets = [dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME]

# Make the dataframe a global variable
global df

# import the dataframe json file
df = pd.read_json('https://raw.githubusercontent.com/perfectly-preserved-pie/xenosaga/master/json/episode3.json')

# Create the Dash DataTable
table = dash_table.DataTable(
    columns=[
        {"name": i, "id": i} for i in df.columns
    ],
    data=df.to_dict("records"),
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
    html.H3("Xenosaga Episode III: Also sprach Zarathustra Enemy Database", className="card-title"),
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