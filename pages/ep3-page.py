from dash import dash_table, dash, html
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
df = pd.read_json('/json/episode2.json')