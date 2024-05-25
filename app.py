from dash import Dash, dcc, html, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from loguru import logger
import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd

external_stylesheets = [
  dbc.icons.BOOTSTRAP,
  dbc.icons.FONT_AWESOME,
  dbc.themes.DARKLY,
  "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css", # https://github.com/AnnMarieW/dash-bootstrap-templates#dbccss--stylesheet

]

ep1_df = pd.read_json('assets/json/episode1.json', lines=True) # Read the JSON files into dataframes 
ep2_df = pd.read_json('assets/json/episode2.json', lines=True)
ep3_df = pd.read_json('assets/json/episode3.json', lines=True)

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
app.description = "A searchable and sortable table of all enemies in the Xenosaga series, organized by game."

title_card = dbc.Card(
  [
    html.H3("Xenosaga Enemy Database", className="card-title"),
    html.I("Mystic powers, grant me a miracle! ✨", style={"margin-bottom": "10px"}),
    html.P(
      "This is a mobile-friendly searchable, sortable, and filterable table of all enemies in the Xenosaga series, organized by game.",
      style = {"margin-bottom": "0px"}
    ),
    html.P(
      "Clicking on anywhere on a row will display the selected enemy's stats in a popup.",
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
  ],
  body = True
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
    dcc.Store(id='active-tab-data'),
    html.Div(title_card),
    # Use dcc.Tabs for episode selection instead of buttons
    dbc.Tabs(
      id='tabs',
      active_tab='ep1',  # Set default active tab to Episode I
      children=[
        dbc.Tab(label='Episode I', tab_id='ep1'),
        dbc.Tab(label='Episode II', tab_id='ep2'),
        dbc.Tab(label='Episode III', tab_id='ep3'),
      ],
      style={'flex': '0 0 auto'},  # Style adjustments for tabs
    ),
    # Container for the grid; make sure it's visible and properly styled
    html.Div(
      dag.AgGrid(
        id='grid',
        className="ag-theme-alpine-dark",
        style={'width': '100%', 'height': 'calc(100vh - 200px)'},  # Adjust height as needed
      ),
      id='grid-container',
      style={'flex': '1 1 auto', 'overflow': 'hidden'},  # Adjusted style for proper overflow handling
    ),
    modal,
  ],
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
  
  # Create the column definitions
  # The Name column is special because it's the only column that's pinned to the left
  column_defs = [
    {
      "field": "Name",  # Set the field to "Name" for the Name column
      "minWidth": 150,  # Set a minimum width for the Name column
      "pinned": "left",  # Pin the Name column to the left
      "resizable": True,
      "sortable": True,
      "type": "textColumn",
      "filter": "agTextColumnFilter",
      "floatingFilter": True,
      "floatingFilterComponentParams": {"filterPlaceholder": "Search..."},
      "suppressMenu": True
    }
  ]
  # Add other columns except the "Name" or "uuid" column
  for i in df.columns:
    if i not in ["Name", "uuid"]:
      column_def = {
        "field": i,
        "filter": "agNumberColumnFilter" if is_numeric_col(df, i) else "agTextColumnFilter",
        "floatingFilter": True,
        "floatingFilterComponentParams": {"suppressFilterButton": False} if is_numeric_col(df, i) else {"filterPlaceholder": "Search..."},
        "minWidth": 120,
        "resizable": True,
        "sortable": True,
        "suppressMenu": True,
        "tooltipField": i, # Set the tooltip field to the column name
        "type": "numericColumn" if is_numeric_col(df, i) else "textColumn",
        "valueFormatter": {"function": "d3.format(',.0f')(params.value)"} if is_numeric_col(df, i) else None,
        "valueGetter": get_value_getter(i),
      }
      # Only add tooltipComponent for string columns
      if not is_numeric_col(df, i):
        column_def["tooltipComponent"] = "CustomTooltip"
      
      column_defs.append(column_def)
        
  return column_defs

# A callback to generate the grid (lazy load) and the column definitions based on the selected tab
@app.callback(
  [Output('grid', 'rowData'), Output('grid', 'columnDefs'), Output('active-tab-data', 'data')],
  [Input('tabs', 'active_tab')]
)
def update_grid_data_and_columns(active_tab):
  if active_tab == 'ep1':
    data = ep1_df
  elif active_tab == 'ep2':
    data = ep2_df
  elif active_tab == 'ep3':
    data = ep3_df
  else: # Handle the case where the active tab is not one of the above
    return [], []  # Return empty data and column definitions

  rowData = data.to_dict('records')
  columnDefs = generate_column_defs(data)
  return rowData, columnDefs, rowData


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
  ],
  [
    State("modal", "is_open"),
    State("grid", "rowData")
  ]
)
def open_and_populate_modal(cell_clicked_data, close_btn_clicks, modal_open, grid_data):
  ctx = dash.callback_context

  if not ctx.triggered:
    return no_update, no_update

  trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

  if trigger_id == 'close':
    return False, no_update

  if trigger_id == 'grid':
    if not cell_clicked_data or 'rowIndex' not in cell_clicked_data:
      raise PreventUpdate

    # Assuming 'rowId' corresponds to the index in 'grid_data' and contains the 'uuid'
    row_id = cell_clicked_data['rowId']
    clicked_uuid = grid_data[int(row_id)]['uuid']

    # Populate the modal with the correct data
    data = {"uuid": clicked_uuid}
    if not data:
      raise PreventUpdate

    # Consolidate dataset lookup into a single statement with a clearer structure
    datasets = {'ep1': ep1_df, 'ep2': ep2_df, 'ep3': ep3_df}
    found_df = next((df for df_name, df in datasets.items() if data["uuid"] in df['uuid'].values), None)

    if found_df is None:
      logger.error(f"UUID {data['uuid']} not found in any dataset.")
      return True, html.P("Error: Details not found for the selected enemy.", className="modal-error-message")

    # Efficiently retrieve the selected row
    selected_row = found_df.loc[found_df['uuid'] == data['uuid']].iloc[0]

    def format_value(value):
      """Format the value for display. If the value is a number, format it with commas. Otherwise, return the value as is."""
      if value is None or value == '':
        return 'N/A'
      try:
        numeric_value = float(value)
        if numeric_value.is_integer():
          return f"{int(numeric_value):,}"
        return f"{numeric_value:,}"
      except (ValueError, TypeError):
        return value
      
    def apply_element_style(text):
      """Colorize the text based on the element. Preserves spaces and commas."""
      color_styles = {
        "Lightning": "yellow",
        "Fire": "red",
        "Ice": "lightblue"
      }
      parts = text.split(", ")
      spans = []
      for i, part in enumerate(parts):
        color = color_styles.get(part, None)
        if color:
          spans.append(html.Span(part, style={'color': color}))
        else:
          spans.append(html.Span(part))
        if i < len(parts) - 1:
          spans.append(", ")
      return spans


    # Streamline content generation by using Dash HTML components for better layout control
    content = []
    for key, value in selected_row.items():
      if key != "uuid":
        if isinstance(value, str):
          spans = apply_element_style(value)
          content.append(html.Div([html.B(f"{key}: "), *spans], style={'margin-bottom': '10px'}))
        else:
          content.append(html.Div([html.B(f"{key}: "), html.Span(f"{format_value(value) if pd.notnull(value) else 'N/A'}")], style={'margin-bottom': '10px'}))

    logger.debug(f"Selected enemy stats: {content}")

    return True, html.Div(content, className="modal-content-wrapper")

  return no_update, no_update

# Run the app if running locally
if __name__ == '__main__':
  app.run_server(debug=True)