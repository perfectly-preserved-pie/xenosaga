import pandas as pd

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