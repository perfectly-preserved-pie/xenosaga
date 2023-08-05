from dash import Dash, dcc, html, no_update, ctx
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import logging
from pages import ep1, ep2, ep3
import pandas as pd
import dash_ag_grid as dag

logging.getLogger().setLevel(logging.INFO)

external_stylesheets = [
  dbc.icons.BOOTSTRAP,
  dbc.icons.FONT_AWESOME,
  dbc.themes.DARKLY,
  "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css", # https://github.com/AnnMarieW/dash-bootstrap-templates#dbccss--stylesheet

]

ep1_df = pd.read_json('json/episode1.json') # Read the JSON files into dataframes 
ep2_df = pd.read_json('json/episode2.json')
ep3_df = pd.read_json('json/episode3.json')

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
  use_pages=True,
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

title_card = dbc.Card(
  [
    html.H3("Xenosaga Enemy Database", className="card-title"),
    html.I("Mystic powers, grant me a miracle! ✨", style={"margin-bottom": "10px"}),
    html.P(
      "This is a mobile-optimized searchable, sortable, and filterable table of all enemies in the Xenosaga series, separated by game.",
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

tabs = dcc.Tabs(
  id="tabs",
  value='/',
  children=[
    dcc.Tab(label='Episode I', value='/'),
    dcc.Tab(label='Episode II', value='/ep2'),
    dcc.Tab(label='Episode III', value='/ep3'),
  ],
)

# Inside app.layout
modal = dbc.Modal(
  [
    dbc.ModalHeader("Selected Row Information"),
    dbc.ModalBody(id="modal-content"),
    dbc.ModalFooter(
        dbc.Button("Close", id="close", className="ml-auto", n_clicks=0)
    ),
  ],
  id="modal",
  is_open=False,
)

# For Gunicorn
server = app.server

app.layout = html.Div([
  dcc.Location(id='url', refresh=False),
  html.Div(title_card),
  html.Div([
    dbc.Button("Episode I", id='btn-ep1', className="mr-2"),
    dbc.Button("Episode II", id='btn-ep2', className="mr-2"),
    dbc.Button("Episode III", id='btn-ep3', className="mr-2"),
  ]),
  html.Div(id='grid-container'),
  modal,
  # Add a hidden grid in the initial layout
  html.Div(dag.AgGrid(id='grid'), style={'display': 'none'}),
])

# Create a function to generate the column definitions based on the dataframe
def generate_column_defs(df):
  numeric_cols = ['HP', 'EXP', 'TP', 'EP', 'SP', 'Cash'] if 'Cash' in df.columns else []

  def get_value_getter(column_name):
    if column_name in numeric_cols:
      return {"function": f"return params.data.{column_name} && params.data.{column_name}.split('-')[0] ? Number(params.data.{column_name}.split('-')[0]) : null"}
    else:
      return None
  
  column_defs = [
    {
      "field": i,
      "type": "numericColumn",
      "filter": "agNumberColumnFilter",
      # Insert commas in the numeric columns
      "valueFormatter": {"function": "d3.format(',.0f')(params.value)"},
      "valueGetter": get_value_getter(i),
    } if i in numeric_cols else {
      "field": i,
      "type": "textColumn",
      "filter": "agTextColumnFilter",
      "floatingFilter": True,
      "suppressMenu": True,
      "filterParams": {
        "filterPlaceholder": "Search...",
      },
    } for i in df.columns
  ]
  
  return column_defs


@app.callback(
  Output('grid-container', 'children'),
  [
    Input('btn-ep1', 'n_clicks'),
    Input('btn-ep2', 'n_clicks'),
    Input('btn-ep3', 'n_clicks')
  ]
)
def update_grid(n1, n2, n3):
  ctx = dash.callback_context
  if not ctx.triggered:
    data = ep1_df  # default data
  else:
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'btn-ep1':
      data = ep1_df
    elif button_id == 'btn-ep2':
      data = ep2_df
    elif button_id == 'btn-ep3':
      data = ep3_df

  return dag.AgGrid(
    id='grid',
    rowData=data.to_dict('records'),
    columnDefs=generate_column_defs(data),
    columnSize="autoSize",
    className="ag-theme-alpine-dark",
    # ...other grid parameters...
  )

# Create a callback to open a modal when a row is selected in the grid
# Based on https://dashaggrid.pythonanywhere.com/other-examples/popup-from-cell-click
@app.callback(
  Output("modal", "is_open"),
  Output("modal-content", "children"),
  [
    Input("grid", "cellClicked"),
    Input("close", "n_clicks")
  ],
  [State("grid", "rowData")]
)
def open_modal(cell_clicked_data, _, row_data):
  if not cell_clicked_data:  # if no cell is clicked, don't update the modal
    return dash.no_update, dash.no_update

  ctx = dash.callback_context
  button_id = ctx.triggered[0]['prop_id'].split('.')[0]

  if button_id == "close":
    return False, dash.no_update

  # Get the row data of the clicked cell
  selected_row_data = row_data[cell_clicked_data["rowIndex"]]

  # Generate the Markdown content dynamically based on the columns in the selected row data
  content = []
  for key, value in selected_row_data.items():
    content.append(f"**{key}:** {value}  \n")

  return True, dcc.Markdown(''.join(content))

# Run the app
app.run_server(debug=True)