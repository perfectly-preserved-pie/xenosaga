from dash import Dash, html, dcc, dash_table
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
    html.P("This is a searchable and sortable table of all enemies in the Xenosaga series, separated by game."),
    html.P("Click on the other tabs to see enemy list for the other games."),
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
#ep2_df = pd.read_json('json/episode2.json')
ep3_df = pd.read_json('json/episode3.json')

# Create a style for highlighting the selected cell's row
# https://community.plotly.com/t/dash-datatable-press-on-cell-should-highlight-row/44076/2?u=the.oldest.house
style_data_conditional = [
    {
        "if": {"state": "active"},
        "backgroundColor": "rgba(150, 180, 225, 0.2)",
        "border": "1px solid blue",
    },
    {
        "if": {"state": "selected"},
        "backgroundColor": "rgba(0, 116, 217, .03)",
        "border": "1px solid blue",
    },
]

ep1_numeric_cols = ['HP', 'EXP', 'TP', 'EP', 'SP', 'Cash']

# Create the Dash AgGrid for episode 1
ep1_grid = dag.AgGrid(
  id = "ep1_grid",
  rowData = ep1_df.to_dict("records"),
  #columnDefs = [{"field": i} for i in ep1_df.columns],
  defaultColDef = {
    "resizable": True,
    "sortable": True,
    "filter": True,
    "sort": 'asc'
  },
  columnDefs = [{"field": i, "type": "numericColumn"} if i in ep1_numeric_cols else {"field": i} for i in ep1_df.columns],
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
    "sort": 'asc'
  },
  columnDefs = [{"field": i, "type": "numericColumn"} if ep3_df[i].dtype in ['int64', 'float64', 'Int64'] else {"field": i, "sortable": True, "sort": "asc"} if i == "Name" else {"field": i, "sortable": True} for i in ep3_df.columns],
  columnSize = "autoSize",
  className = "ag-theme-alpine-dark",
)

# Create the tab content
tab_1 = html.Div(children=[ep1_grid])
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
        )
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
    elif tab == "ep3":
        return tab_3

# Create a callback to highlight the selected row
@app.callback(    
      Output("datatable-interactivity", "style_data_conditional"),
      Input("datatable-interactivity", "active_cell"),    
)
def highlight_row(active_cell):
    style = style_data_conditional.copy()
    if active_cell:
      style.append(
        {
          "if": {"row_index": active_cell["row"]},
          "backgroundColor": "rgba(150, 180, 225, 0.2)",
          "border": "1px solid blue",
        },
      )
    return style

# Run the app
#app.run_server(debug=True)