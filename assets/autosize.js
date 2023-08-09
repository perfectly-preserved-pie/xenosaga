window.autoSizeAllColumns = function(n1, n2, n3, gridId) {
    if (n1 > 0 || n2 > 0 || n3 > 0) {
      var gridDiv = document.getElementById(gridId);
      if (gridDiv) {
        var gridOptions = gridDiv.gridOptions;
        if (gridOptions && gridOptions.columnApi) {
          var allColumnIds = [];
          gridOptions.columnApi.getAllColumns().forEach(function (column) {
            allColumnIds.push(column.colId);
          });
          gridOptions.columnApi.autoSizeColumns(allColumnIds);
        }
      }
    }
  }
  