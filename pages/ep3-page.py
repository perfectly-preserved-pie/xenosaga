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

layout = html.Div(children=[
    html.H1(children='This is our Episode 3 page'),

    html.Div(children='''
        This is our Ep3 page content.
    '''),
])