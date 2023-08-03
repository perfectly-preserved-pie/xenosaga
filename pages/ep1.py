import dash
from dash import html
import dash_ag_grid as dag
import pandas as pd
import dash_bootstrap_components as dbc

dash.register_page(
  __name__,
  path='/',
  name='Xenosaga Episode I',
  title='Xenosaga Episode I',
  description='ep1 description',
)

external_stylesheets = [
  dbc.icons.BOOTSTRAP,
  dbc.icons.FONT_AWESOME,
  dbc.themes.DARKLY,
  "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css", # https://github.com/AnnMarieW/dash-bootstrap-templates#dbccss--stylesheet
]

ep1_df = pd.read_json('json/episode1.json')

ep1_numeric_cols = ['HP', 'EXP', 'TP', 'EP', 'SP', 'Cash']

# Create a value getter for the numeric columns
# In case the value is a range, use the first number
def get_value_getter(column_name):
  if column_name in ['Cash', 'HP', 'EXP', 'TP', 'SP']:
    return {"function": f"Number(params.data.{column_name}.split('-')[0])"}
  else:
    return None

# Create the Dash AgGrid for episode 1
layout = dag.AgGrid(
    id = "ep1_grid",
    rowData = ep1_df.to_dict("records"),
    #columnDefs = [{"field": i} for i in ep1_df.columns],
    defaultColDef = {
        "resizable": True,
        "sortable": True,
        "filter": True,
    },
    columnDefs = [
        {
        "field": i,
        "type": "numericColumn",
        "filter": "agNumberColumnFilter",
        # Insert commas in the numeric columns
        "valueFormatter": {"function": "d3.format(',.0f')(params.value)"},
        "valueGetter": get_value_getter(i),
        } if i in ep1_numeric_cols else {
        "field": i,
        "type": "textColumn",
        "filter": "agTextColumnFilter",
        "floatingFilter": True,
        "suppressMenu": True,
        "filterParams": {
            "filterPlaceholder": "Search...",
        },
        } for i in ep1_df.columns
    ],
    columnSize = "autoSize",
    className = "ag-theme-alpine-dark",
)