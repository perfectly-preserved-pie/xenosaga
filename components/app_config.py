from dash import Dash
from typing import List, Dict
import dash_bootstrap_components as dbc

external_stylesheets = [
  dbc.icons.BOOTSTRAP,
  dbc.icons.FONT_AWESOME,
  dbc.themes.DARKLY,
  "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css", # https://github.com/AnnMarieW/dash-bootstrap-templates#dbccss--stylesheet

]

# Create the Dash app using a factory function
# This lets me use the same app configuration in multiple files without causing circular imports
def create_app(external_stylesheets: List[str], external_scripts: List[Dict[str, str]]) -> Dash:
  """
  Create and configure the Dash app.

  Args:
    external_stylesheets (List[str]): List of external stylesheets to be used.
    external_scripts (List[Dict[str, str]]): List of external scripts to be used. Each script is represented as a dictionary.

  Returns:
    Dash: The configured Dash app.
  """
  app = Dash(
    __name__,
    assets_folder='../assets',
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    use_pages=False,
    suppress_callback_exceptions=True,
    meta_tags = [
      {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
  )
  return app