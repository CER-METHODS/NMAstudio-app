
import dash_ag_grid as dag
import os
import pandas as pd

data_absolute = {
    'Outcome 1': ['Enter a value'],
    'Outcome 2': ['Enter a value']
}

data_absolute = pd.DataFrame(data_absolute)

absolueColumnDefs = [
   
    {"headerName": "Outcome 1", 
     "field": "Outcome 1",
     "editable": True,
     "resizable": False,
     'cellStyle': {
        'color': 'grey','border-right': 'solid 0.8px'}
     },

    {"headerName": "Outcome 2", 
     "field": "Outcome 2",
     "editable": True,
     "resizable": False,
     'cellStyle': {
        'color': 'grey','border-right': 'solid 0.8px'}
     }
]



outcome_absolute = dag.AgGrid(
    id="grid_absolute",
    className="absolute-alpine color-fonts",
    # enableEnterpriseModules=True,
    # licenseKey=os.environ["AG_GRID_KEY"],
    columnDefs=absolueColumnDefs,
    rowData = data_absolute.to_dict("records"),
    dangerously_allow_code=True,
    defaultColDef={
                    'filter':False,
                    "floatingFilter": False,
                    "wrapText": True, 
                    'autoHeight': True,
                    "enableRowGroup": False,
                    "enableValue": False,
                    "enablePivot": False,
                    'cellStyle': {'white-space': 'pre',
                                  'display': 'grid',
                                  'text-align': 'center',
                                  'align-items': 'center',
                                  'border-bottom': 'solid 0.5px'
                                  },
                    # "tooltipComponent": "CustomTooltip"
                    },
    columnSize="sizeToFit", 
    getRowId='params.data.Reference',
    style={"height":"58px"}
    
)