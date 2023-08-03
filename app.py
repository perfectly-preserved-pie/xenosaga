from dash import Dash, dcc, html, no_update, ctx
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import logging
from pages import ep1, ep2, ep3

logging.getLogger().setLevel(logging.INFO)

external_stylesheets = [
  dbc.icons.BOOTSTRAP,
  dbc.icons.FONT_AWESOME,
  dbc.themes.DARKLY,
  "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css", # https://github.com/AnnMarieW/dash-bootstrap-templates#dbccss--stylesheet

]

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
  tabs,
  html.Div(id='page-content')
])

@app.callback(
  Output('url', 'pathname'),
  Input('tabs', 'value')
)
def on_tab_click(value):
  return value

# Define callback to update page layout
@app.callback(
  Output('page-content', 'children'),
  Input('url', 'pathname')
)
def display_page(pathname):
  if pathname == '/ep2':
    return ep2.layout()
  elif pathname == '/ep3':
    return ep3.layout()
  else:
    return ep1.layout()
  
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
app.run_server(debug=True)