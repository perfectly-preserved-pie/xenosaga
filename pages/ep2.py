import dash
import dash_ag_grid as dag
import pandas as pd
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
  __name__,
  path='/ep2',
  name='Xenosaga Episode II',
  title='Xenosaga Episode II',
  description='ep2 description',
)

external_stylesheets = [
  dbc.icons.BOOTSTRAP,
  dbc.icons.FONT_AWESOME,
  dbc.themes.DARKLY,
  "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css", # https://github.com/AnnMarieW/dash-bootstrap-templates#dbccss--stylesheet
]

ep2_df = pd.read_json('json/episode2.json')

# Create the Dash AgGrid for episode 2
layout = dag.AgGrid(
  id = "ep2_grid",
  rowData = ep2_df.to_dict("records"),
  #columnDefs = [{"field": i} for i in ep2_df.columns],
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
    } if pd.api.types.is_numeric_dtype(ep2_df[i]) == True else {
      "field": i,
      "type": "textColumn",
      "filter": "agTextColumnFilter",
      "floatingFilter": True,
      "suppressMenu": True,
      "filterParams": {
        "filterPlaceholder": "Search...",
      },
    } for i in ep2_df.columns
  ],
  columnSize = "autoSize",
  className = "ag-theme-alpine-dark",
)