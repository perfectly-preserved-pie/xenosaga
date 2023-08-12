from dash import Dash, dcc, html, no_update, ctx
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import logging
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)

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
  dcc.Store(id='clicked-cell-unique-value'),
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
  },
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
      "field": "Name",  # Set the field to "Name" for the Name column
      "type": "textColumn",
      "sortable": True,
      "resizable": True,
      "minWidth": 150,  # Set a minimum width for the Name column
      "pinned": "left",  # Pin the Name column to the left
    }
  ]
  # Add other columns except the "Name" column
  for i in df.columns:
    if i != "Name":
      column_def = {
        "field": i,
        "type": "numericColumn" if is_numeric_col(df, i) else "textColumn",
        "filter": "agNumberColumnFilter" if is_numeric_col(df, i) else "agTextColumnFilter",
        "suppressMenu": True,
        "valueFormatter": {"function": "d3.format(',.0f')(params.value)"} if is_numeric_col(df, i) else None,
        "valueGetter": get_value_getter(i),
        "minWidth": 120,
        "resizable": True,
        "sortable": True,
        "floatingFilter": True,
        "floatingFilterComponentParams": {"suppressFilterButton": False} if is_numeric_col(df, i) else {"filterPlaceholder": "Search..."},
      }
      column_defs.append(column_def)
        
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
  Output("clicked-cell-unique-value", "data"),
  [
    Input("grid", "cellClicked"),
    Input("close", "n_clicks"),
  ],
  [State("modal", "is_open"), State("grid", "rowData")]
)
def open_modal(cell_clicked_data, close_btn_clicks, modal_open, grid_data):
  ctx = dash.callback_context
  if not ctx.triggered:
    return dash.no_update, dash.no_update

  button_id = ctx.triggered[0]['prop_id'].split('.')[0]

  if button_id == 'close':
    return False, dash.no_update

  elif button_id == 'grid':
    if not cell_clicked_data or 'rowIndex' not in cell_clicked_data:
      raise PreventUpdate

    # Extract the name of the clicked enemy using rowId
    row_id = cell_clicked_data['rowId']
    clicked_name = grid_data[int(row_id)]['Name']
    return True, {"name": clicked_name}

  else:
    raise PreventUpdate

# Create a callback to populate the modal with the correct data
@app.callback(
  Output("modal-content", "children"),
  [Input("clicked-cell-unique-value", "data")],
  [State("btn-ep1", "n_clicks"), State("btn-ep2", "n_clicks"), State("btn-ep3", "n_clicks")]
)
def populate_modal(data, n1, n2, n3):
  if not data:
    raise PreventUpdate

  # Determine the correct dataframe based on the clicked episode button
  clicks = {
    'btn-ep1': n1 or 0,  # Default to 0 if None
    'btn-ep2': n2 or 0,
    'btn-ep3': n3 or 0
  }
  latest_button = max(clicks, key=clicks.get)

  if latest_button == 'btn-ep1':
    df = ep1_df
  elif latest_button == 'btn-ep2':
    df = ep2_df
  elif latest_button == 'btn-ep3':
    df = ep3_df

  # Check if the desired name exists in the dataset
  selected_rows = df[df["Name"] == data["name"]]
  if selected_rows.empty:
    logging.error(f"Name {data['name']} not found in dataset.")
    raise PreventUpdate

  selected_row = selected_rows.iloc[0]
  logging.info(f"Selected Row Data: {selected_row}")  # Log the complete row data

  content = []
  for key, value in selected_row.items():
    if pd.api.types.is_numeric_dtype(value) and pd.notna(value):  # Check if value is numeric and not NaN
      formatted_value = f"{int(value):,}"  # Format as integer with thousands separator
    else:
      formatted_value = "N/A" if pd.isna(value) else value  # Replace NaN with "N/A", otherwise use value as-is
        
    logging.info(f"Key: {key}, Formatted Value: {formatted_value}")  # Log each key-value pair
    content.append(f"**{key}:** {formatted_value}  \n")  # Use two spaces and a newline character for separate lines

  generated_content = ''.join(content)
  logging.info(f"Generated Content: {generated_content}")  # Log the generated content
  return dcc.Markdown(generated_content)

# Run the app
#app.run_server(debug=True)