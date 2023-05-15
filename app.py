from dash import Dash, html, dcc, ctx, dash
from dash.dependencies import Input, Output
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import logging
import pandas as pd

logging.getLogger().setLevel(logging.INFO)

external_stylesheets = [
  dbc.icons.BOOTSTRAP,
  dbc.icons.FONT_AWESOME,
  dbc.themes.DARKLY,
  "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css", # https://github.com/AnnMarieW/dash-bootstrap-templates#dbccss--stylesheet

]

# Make the dataframe a global variable
global df

app = Dash(
  __name__, 
  external_stylesheets=external_stylesheets,
  external_scripts=[
    # Plausible analytics
    {
      'src': "https://plausible.automateordie.io/js/plausible.js",
      'data-domain': "enemies.xenosaga.games",
      'defer': True,
      'type': 'application/javascript'
    },
  ],
  use_pages=False,
  # Because we're displaying tab content dynamically, we need to suppress callback exceptions
  # https://dash.plotly.com/callback-gotchas#callbacks-require-all-inputs-and-states-to-be-rendered-on-the-page
  suppress_callback_exceptions=True, 
  # Add meta tags for mobile devices
  # https://community.plotly.com/t/reorder-website-for-mobile-view/33669/5?
  meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
  ],
)

# Set the page title
app.title = "Xenosaga Enemy Database"
app.description = "A searchable and sortable table of all enemies in the Xenosaga series, separated by game."

# For Gunicorn
server = app.server

title_card = dbc.Card(
  [
    html.H3("Xenosaga Enemy Database", className="card-title"),
    html.I("Mystic powers, grant me a miracle! ✨", style={"margin-bottom": "10px"}),
    html.P(
      "This is a searchable and sortable table of all enemies in the Xenosaga series, separated by game.",
      style = {"margin-bottom": "0px"}
    ),
    html.P(
      "Click on the other tabs to see enemy list for the other games.",
      style = {"margin-bottom": "0px"}
    ),
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

# Create the tabs
tabs = dcc.Tabs(
  id="tabs",
  value="ep1",
  children=[
    dcc.Tab(label="Xenosaga Episode I", value="ep1"),
    dcc.Tab(label="Xenosaga Episode II", value="ep2"),
    dcc.Tab(label="Xenosaga Episode III", value="ep3"),
  ]
)

# Create the tables
# import the dataframe json file
ep1_df = pd.read_json('json/episode1.json')
ep2_df = pd.read_json('json/episode2.json')
ep3_df = pd.read_json('json/episode3.json')

ep1_numeric_cols = ['HP', 'EXP', 'TP', 'EP', 'SP', 'Cash']
# Create a value getter for the numeric columns
# In case the value is a range, use the first number
def get_value_getter(column_name):
  if column_name in ['Cash', 'HP', 'EXP', 'TP', 'SP']:
    return {"function": f"Number(params.data.{column_name}.split('-')[0])"}
  else:
    return None

# Create the Dash AgGrid for episode 1
ep1_grid = dag.AgGrid(
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
  dashGridOptions={"rowSelection": "single"},
  columnSize = "autoSize",
  className = "ag-theme-alpine-dark",
)

# Create the Dash AgGrid for episode 2
ep2_grid = dag.AgGrid(
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

# Create the Dash AgGrid for episode 3
ep3_grid = dag.AgGrid(
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

# Create the tab content
tab_1 = html.Div(children=[ep1_grid])
tab_2 = html.Div(children=[ep2_grid])
tab_3 = html.Div(children=[ep3_grid])

# Create the home page layout
app.layout = dbc.Container([
  dbc.Row( # First row: title card
    [
      dbc.Col([title_card]),
    ]
  ),
  dbc.Row( # Second row: tabs/tables
    html.Div(
      [
        dbc.Col(
          [
            tabs,
            html.Div(id="tab-content")
          ]
        ),
        dbc.Modal(
          [
            dbc.ModalHeader("More information about selected enemy"),
            dbc.ModalBody(id="modal-content"),
            dbc.ModalFooter(dbc.Button("Close", id="close", className="ml-auto")),
          ],
          id="modal",
        ),
      ]
    ),
  ),
],
fluid=True,
className = "dbc dbc-row-selectable"
)

# Create the callback to update the tab content
@app.callback(
  Output("tab-content", "children"),
  [Input("tabs", "value")]
)
def render_content(tab):
  if tab == "ep1":
    return tab_1
  elif tab == "ep2":
    return tab_2
  elif tab == "ep3":
    return tab_3

# Create a callback to open a modal when a row is selected in the episode 1 grid
# Based on https://dashaggrid.pythonanywhere.com/other-examples/popup-from-cell-click
@app.callback(
  Output("modal", "is_open"),
  Output("modal-content", "children"),
  Input("ep1_grid", "selectedRows"),
  Input("close", "n_clicks"),
)
def open_modal(selection, _):
  if ctx.triggered_id == "close":
    return False, dash.no_update
  if selection:
    # Use Markdown to format the modal content
    return True, dcc.Markdown(f""" 
      **Name:** {selection[0]['Name']}  \n
      **HP:** {selection[0]['HP']}  \n
      **EXP:** {selection[0]['EXP']}  \n
      **TP:** {selection[0]['TP']}  \n
      **EP:** {selection[0]['SP']}  \n
      **SP:** {selection[0]['SP']}  \n
      **Cash:** {selection[0]['Cash']}  \n
      **Normal Drop:** {selection[0]['Normal Drop']}  \n
      **Rare Drop:** {selection[0]['Rare Drop']}  \n
      **Type:** {selection[0]['Type']}  \n
      **Weakness:** {selection[0]['Weakness']}  \n
      """)
  return dash.no_update, dash.no_update

# Run the app
#app.run_server(debug=True)