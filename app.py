from dash import Dash, dcc, html
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import logging

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
  #suppress_callback_exceptions=True, 
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

# For Gunicorn
server = app.server

app.layout = dbc.Container([
  dbc.Row( # First row: title card
    [
      dbc.Col(
        title_card,
        width = 12,
      ),
    ],
    className="g-0",
  ),
  dbc.Row( # Second row: the rest
    [
	    dash.page_container
    ],
    # Remove the whitespace/padding between the two cards (aka the gutters)
    # https://stackoverflow.com/a/70495385
    className="g-0",
  ),
#html.Link(href='/assets/style.css', rel='stylesheet'),
],
fluid = True,
className = "dbc",
)

# Run the app
app.run_server(debug=True)