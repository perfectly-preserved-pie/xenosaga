from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import logging
import pandas as pd

logging.getLogger().setLevel(logging.INFO)

external_stylesheets = [dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME]

# Make the dataframe a global variable
global df

app = Dash(
  __name__, 
  external_stylesheets=external_stylesheets,
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

# Plausible privacy-friendly analytics
# https://dash.plotly.com/external-resources#usage (Option 1)
# Probably won't get past adblockers and NoScript but whatever, good enough
app.index_string = """<!DOCTYPE html>
<html>
  <head>
    <script defer data-domain="xenosaga.automateordie.io" src="https://plausible.automateordie.io/js/plausible.js" type="application/javascript"></script>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
  </head>
  <body>
    {%app_entry%}
    <footer>
      {%config%}
      {%scripts%}
      {%renderer%}
    </footer>
  </body>
</html>
"""

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
ep1_df = pd.read_json('https://raw.githubusercontent.com/perfectly-preserved-pie/xenosaga/master/json/episode1.json')
#ep2_df = pd.read_json('https://raw.githubusercontent.com/perfectly-preserved-pie/xenosaga/master/json/episode2.json')
ep3_df = pd.read_json('https://raw.githubusercontent.com/perfectly-preserved-pie/xenosaga/master/json/episode3.json')

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

# Create the Dash DataTable for episode 1
ep1_table = dash_table.DataTable(
    columns=[
        {"name": i, "id": i} for i in ep1_df.columns
    ],
    data=ep1_df.to_dict("records"),
    id='datatable-interactivity',
    filter_action="native",
    filter_options={
        'case': 'insensitive',
        'placeholder_text': 'Type a string to search...'
    },
    sort_action="native",
    style_data_conditional=style_data_conditional
)

# Create the Dash DataTable for episode 3
ep3_table = dash_table.DataTable(
    columns=[
        {"name": i, "id": i} for i in ep3_df.columns
    ],
    data=ep3_df.to_dict("records"),
    tooltip_delay=0,
    tooltip_duration=None,
    id='datatable-interactivity',
    filter_action="native",
    filter_options={
        'case': 'insensitive',
        'placeholder_text': 'Type a string to search...'
    },
    sort_action="native",
    style_data_conditional=style_data_conditional
)

# Create the tab content
tab_1 = html.Div(children=[ep1_table])
tab_3 = html.Div(children=[ep3_table])

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
className = "dbc"
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
app.run_server(debug=True)