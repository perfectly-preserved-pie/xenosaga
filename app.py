from dash import Dash, dcc, html, no_update, ctx
from dash.dependencies import Input, Output, State
import dash
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
  use_pages=False,
  # Because we're displaying tab content dynamically, we need to suppress callback exceptions
  # https://dash.plotly.com/callback-gotchas#callbacks-require-all-inputs-and-states-to-be-rendered-on-the-page
  suppress_callback_exceptions=True, 
  # Add meta tags for mobile devices
  # https://community.plotly.com/t/reorder-website-for-mobile-view/33669/5?
  meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    # Set CSP to allow AG Grid to work
    # See https://www.ag-grid.com/javascript-data-grid/security/#summary
    {"http-equiv": "Content-Security-Policy", "content": "default-src 'self'; script-src 'self' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src data:"}
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
        "margin-left": "0px"
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

# Create a modal to display the selected enemy stats
# The modal will be populated by the callback below
modal = dbc.Modal(
  [
    dbc.ModalHeader("Selected Enemy Stats"),
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

app.layout = html.Div(
  [
  dcc.Location(id='url', refresh=False),
  html.Div(title_card),
  html.Div([
    dbc.Button("Episode I", id='btn-ep1', className="mr-2"),
    dbc.Button("Episode II", id='btn-ep2', className="mr-2"),
    dbc.Button("Episode III", id='btn-ep3', className="mr-2"),
  ]),
  html.Div(id='grid-container', style={'flex': '1'}),
  modal,
  # Add a hidden grid in the initial layout
  html.Div(dag.AgGrid(id='grid'), style={'display': 'none'}),
  ],
  # Set the flexbox direction to column
  # This will make the grid fill the entire page
  style={
    'display': 'flex',
    'flexDirection': 'column',
    'height': '100vh'
  }
)


# Create a function to generate the column definitions based on the dataframe
def generate_column_defs(df):
  # Determine if a column is numeric based on a sampling of 100 values from the column
  # I did this way because I'm too lazy to properly cast dtypes for the 30+ columns across all 3 episode dataframes
  def is_numeric_col(df, column_name):
    # If dtype is already numeric, return True
    if pd.api.types.is_numeric_dtype(df[column_name].dtype):
      return True
    # If dtype is object, sample some rows and test if they can be converted to numbers
    non_na_values = df[column_name].dropna() # Drop NA values
    sample_values = non_na_values.sample(min(100, len(non_na_values))).tolist()
    try:
      # Try converting the sample values to numbers
      [float(x) for x in sample_values]
      return True
    except ValueError:
      # If conversion fails, it's not a numeric column
      return False

  # Extracts the starting number from a cell's content, especially if the content represents a range like "100-200"
  # This is used to sort the numeric columns properly
  def get_value_getter(column_name):
    if is_numeric_col(df, column_name):
      return {"function": f"return params.data.{column_name} && params.data.{column_name}.split('-')[0] ? Number(params.data.{column_name}.split('-')[0]) : null"}
    else:
      return None
  
  column_defs = [
    {
      "field": i,
      "type": "numericColumn" if is_numeric_col(df, i) else "textColumn",
      "filter": "agNumberColumnFilter" if is_numeric_col(df, i) else "agTextColumnFilter",
      "suppressMenu": True,
      # Insert commas in the numeric columns
      "valueFormatter": {"function": "d3.format(',.0f')(params.value)"} if is_numeric_col(df, i) else None,
      "valueGetter": get_value_getter(i),
      "minWidth": 120,  # Minimum width of 100 pixels
      "resizable": True,
      "sortable": True,
      "floatingFilter": True,
      "floatingFilterComponentParams": {"suppressFilterButton": False} if is_numeric_col(df, i) else {"filterPlaceholder": "Search..."},
    } for i in df.columns
  ]
  return column_defs

# A callback to generate the grid
@app.callback(
  Output('grid-container', 'children'),
  Output('grid', 'rowData'),
  Output('grid', 'columnDefs'),
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

  grid = dag.AgGrid(
    id='grid',
    rowData=data.to_dict('records'),
    columnDefs=generate_column_defs(data),
    className="ag-theme-alpine-dark",
    style={'height': '100%'}
    # ...other grid parameters...
  )

  return grid, data.to_dict('records'), generate_column_defs(data)

# Create a callback to update the column size to autoSize
# Gets triggered when the columnDefs property of the grid changes. This callback will then set the columnSize property to "autoSize"
@app.callback(
  Output('grid', 'columnSize'),
  [Input('grid', 'columnDefs')]
)
def update_column_size(_):
  return "responsiveSizeToFit"

# Create a callback to open a modal when a row is selected in the grid
# Based on https://dashaggrid.pythonanywhere.com/other-examples/popup-from-cell-click
@app.callback(
  Output("modal", "is_open"),
  Output("modal-content", "children"),
  [
    Input("grid", "cellClicked"),
    Input("close", "n_clicks"),
    State("grid", "selectedData")
  ],
  [State("grid", "rowData")]
)
def open_modal(cell_clicked_data, _, selected_data):
  if not cell_clicked_data:  # if no cell is clicked, don't update the modal
    return dash.no_update, dash.no_update

  ctx = dash.callback_context
  button_id = ctx.triggered[0]['prop_id'].split('.')[0]

  if button_id == "close":
    return False, dash.no_update

  clicked_column = cell_clicked_data['colId']  # Get the clicked column name

  # Get the row data of the clicked cell
  selected_row_data = selected_data[0]

  # Generate the Markdown content dynamically based on the columns in the selected row data
  content = []
  for key, value in selected_row_data.items():
    if isinstance(value, (int, float)):
      formatted_value = f"{value:,}"  # Format number with thousands separator
    else:
      formatted_value = value

    # If this is the clicked column, apply special formatting
    if key == clicked_column:
      content.append(f'### {key}: {formatted_value}  \n')
    else:
      content.append(f"**{key}:** {formatted_value}  \n")

  return True, dcc.Markdown(''.join(content))

# Run the app
#app.run_server(debug=True)