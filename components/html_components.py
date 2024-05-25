from dash import html
import dash_bootstrap_components as dbc

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