import dash
import dash_ag_grid as dag
import pandas as pd
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
  __name__,
  path='/ep3',
  name='Xenosaga Episode III',
  title='Xenosaga Episode III',
  description='ep3 description',
)

external_stylesheets = [
  dbc.icons.BOOTSTRAP,
  dbc.icons.FONT_AWESOME,
  dbc.themes.DARKLY,
  "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css", # https://github.com/AnnMarieW/dash-bootstrap-templates#dbccss--stylesheet
]

ep3_df = pd.read_json('json/episode3.json')

layout = dag.AgGrid(
  id = "ep3_grid",
  rowData = ep3_df.to_dict("records"),
  #columnDefs = [{"field": i} for i in ep3_df.columns],
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
    } if pd.api.types.is_numeric_dtype(ep3_df[i]) == True else {
      "field": i,
      "type": "textColumn",
      "filter": "agTextColumnFilter",
      "floatingFilter": True,
      "suppressMenu": True,
      "filterParams": {
        "filterPlaceholder": "Search...",
      },
    } for i in ep3_df.columns
  ],
  columnSize = "autoSize",
  className = "ag-theme-alpine-dark",
)

    
    