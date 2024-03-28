from dash import Dash, dcc, html, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from loguru import logger
import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd

# Read the JSON files into dataframes
ep1_df = pd.read_json('assets/json/episode1.json', lines=True)
ep2_df = pd.read_json('assets/json/episode2.json', lines=True)
ep3_df = pd.read_json('assets/json/episode3.json', lines=True)

external_stylesheets = [
  dbc.icons.BOOTSTRAP,
  dbc.icons.FONT_AWESOME,
  dbc.themes.DARKLY,
  "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css",
]

app = Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=[
  {
    'src': "https://plausible.automateordie.io/js/plausible.js",
    'data-domain': "enemies.xenosaga.games",
    'defer': True,
    'type': 'application/javascript'
  },
], suppress_callback_exceptions=True, meta_tags=[
  {"name": "viewport", "content": "width=device-width, initial-scale=1"}
])

app.title = "Xenosaga Enemy Database"
app.description = "A searchable and sortable table of all enemies in the Xenosaga series, organized by game."

title_card = dbc.Card(
  [
    html.H3("Xenosaga Enemy Database", className="card-title"),
    html.I("Mystic powers, grant me a miracle! ✨", style={"margin-bottom": "10px"}),
    html.P(
      "This is a mobile-friendly searchable, sortable, and filterable table of all enemies in the Xenosaga series, organized by game.",
      style={"margin-bottom": "0px"}
    ),
    html.P(
      "Clicking on anywhere on a row will display the selected enemy's stats in a popup.",
      style={"margin-bottom": "0px"}
    ),
    html.I(className="bi bi-github", style={"margin-right": "5px", "margin-left": "0px"}),
    html.A("GitHub", href='https://github.com/perfectly-preserved-pie/xenosaga', target='_blank'),
  ],
  body=True
)

modal = dbc.Modal(
  [
    dbc.ModalHeader("Selected Enemy Stats"),
    dbc.ModalBody(id="modal-content"),
    dbc.ModalFooter(dbc.Button("Close", id="close", className="ml-auto", n_clicks=0)),
  ],
  id="modal",
  is_open=False,
)

app.layout = html.Div(
  [
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='clicked-cell-unique-value'),
    html.Div(title_card),
    dbc.Tabs(
      id='tabs',
      active_tab='ep1',
      children=[dbc.Tab(label='Episode I', tab_id='ep1'), dbc.Tab(label='Episode II', tab_id='ep2'), dbc.Tab(label='Episode III', tab_id='ep3')],
      style={'flex': '0 0 auto'},
    ),
    html.Div(
      dag.AgGrid(id='grid', className="ag-theme-alpine-dark", style={'width': '100%', 'height': 'calc(100vh - 200px)'}),
      id='grid-container',
      style={'flex': '1 1 auto', 'overflow': 'hidden'},
    ),
    modal,
  ],
  style={'display': 'flex', 'flexDirection': 'column', 'height': '100vh'},
)

def is_numeric_col(df: pd.DataFrame, column_name: str) -> bool:
  non_na_values = df[column_name].dropna()
  sample_values = non_na_values.sample(min(100, len(non_na_values))).tolist()
  try:
    [float(x) for x in sample_values]
    return True
  except ValueError:
    return False

def generate_column_defs(df: pd.DataFrame) -> list:
  column_defs = [{
    "field": "Name",
    "minWidth": 150,
    "pinned": "left",
    "resizable": True,
    "sortable": True,
    "type": "textColumn",
    "filter": "agTextColumnFilter",
    "floatingFilter": True,
    "floatingFilterComponentParams": {"filterPlaceholder": "Search..."},
    "suppressMenu": True
  }]

  for i in df.columns:
    if i not in ["Name", "uuid"]:
      column_def = {
        "field": i,
        "filter": "agNumberColumnFilter" if is_numeric_col(df, i) else "agTextColumnFilter",
        "floatingFilter": True,
        "minWidth": 120,
        "resizable": True,
        "sortable": True,
        "suppressMenu": True,
        "type": "numericColumn" if is_numeric_col(df, i) else "textColumn",
      }
      column_defs.append(column_def)

  return column_defs

@app.callback(
  [Output('grid', 'rowData'), Output('grid', 'columnDefs')],
  [Input('tabs', 'active_tab')]
)
def update_grid_data_and_columns(active_tab: str):
  data = {'ep1': ep1_df, 'ep2': ep2_df, 'ep3': ep3_df}.get(active_tab, pd.DataFrame())
  rowData = data.to_dict('records')
  columnDefs = generate_column_defs(data)
  return rowData, columnDefs

@app.callback(
  Output('grid', 'columnSize'),
  [Input('grid', 'columnDefs')]
)
def update_column_size(_):
  return "responsiveSizeToFit"

@app.callback(
  [Output("modal", "is_open"), Output("clicked-cell-unique-value", "data")],
  [Input("grid", "cellClicked"), Input("close", "n_clicks")],
  [State("modal", "is_open"), State("grid", "rowData")]
)
def toggle_modal(cell_clicked_data, close_btn_clicks, is_modal_open, grid_data):
  ctx = dash.callback_context
  if not ctx.triggered:
    return no_update, no_update
  trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
  if trigger_id == "close":
    return False, no_update
  if trigger_id == "grid":
    if cell_clicked_data and 'rowIndex' in cell_clicked_data:
        row_id = cell_clicked_data['rowId']
        clicked_uuid = grid_data[int(row_id)]['uuid']
        return not is_modal_open, {"uuid": clicked_uuid}
  return no_update, no_update

@app.callback(
  Output("modal-content", "children"),
  [Input("clicked-cell-unique-value", "data")],
  prevent_initial_call=True
)
def update_modal_content(data):
  if not data:
    raise PreventUpdate
  datasets = {'ep1': ep1_df, 'ep2': ep2_df, 'ep3': ep3_df}
  found_df = next((df for df_name, df in datasets.items() if data["uuid"] in df['uuid'].values), None)
  if found_df is None:
    logger.error(f"UUID {data['uuid']} not found in any dataset.")
    return html.P("Error: Details not found for the selected enemy.", className="modal-error-message")
  selected_row = found_df.loc[found_df['uuid'] == data['uuid']].iloc[0]
  content = [html.Div([html.B(f"{key}: "), f"{value if pd.notnull(value) else 'N/A'}"]) for key, value in selected_row.items() if key != "uuid"]
  return html.Div(content, className="modal-content-wrapper")

# Gunicorn server
server = app.server

if __name__ == '__main__':
  app.run_server(debug=True)