
import dash_ag_grid as dag
import os
import pandas as pd
import itertools
import numpy as np
import dash_iconify
import json


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



data = pd.read_csv('db/skt/skt_df_two.csv')
df = pd.DataFrame(data)
# treat_list = np.unique(df.Treatment).tolist()


# combinations = list(itertools.combinations(treat_list, 2))

# treatment = []
# comparator =[]

# for pair in combinations:
#     treatment.append(pair[0])
#     comparator.append(pair[1])

# treat_compare = pd.DataFrame({
#     'treatment': treatment,
#     'comparator': comparator
# })

df['switch']=np.nan

ColumnDefs_treat_compare = [
   
    {"headerName": "Treatment", 
     "field": "Treatment",
     "editable": False,
     "resizable": False,
     'cellStyle': {
        'background-color': '#a6d4a6bd',
        'color':'#04800f'
        }
     },
    
     {"headerName": "Switch", 
     "field": "switch",
     "editable": False,
     "resizable": False,
     "cellRenderer": "DMC_Button",
     "cellRendererParams": {
            # "variant": "text",
            "icon": "subway:round-arrow-3",  # Use 'icon' instead of 'leftIcon' or 'rightIcon'
            "color": "#ffc000",
        },
     'cellStyle': {
        'background-color': 'white'}
     },

    {"headerName": "Comparator", 
     "field": "Reference",
     "editable": False,
     "resizable": False,
     'cellStyle': {
        'background-color': '#ffc1078a',
        'color':'#04800f'
        }
     },
     {
        'headerName': 'Pasi90',
        'headerClass': 'center-aligned-group-header',
        'suppressStickyLabel': True,
        'children': [
            {'field': 'RR'},
            {'field': 'lower'},
        ]
    },
    {
        'headerName': 'SAE',
        'headerClass': 'center-aligned-group-header',
        'suppressStickyLabel': True,
        'children': [
            {'field': 'RR_out2'},
            {'field':'CI_lower_out2'},
        ]
    },
]

treat_compare_grid = dag.AgGrid(
    id="grid_treat_compare",
    className="ag-theme-alpine color-fonts",
    enableEnterpriseModules=True,
    licenseKey=os.environ["AG_GRID_KEY"],
    columnDefs=ColumnDefs_treat_compare,
    rowData = df.to_dict("records"),
    dangerously_allow_code=True,
    defaultColDef={
                    'filter':False,
                    "floatingFilter": False,
                    "wrapText": True, 
                    # 'autoHeight': True,
                    "enableRowGroup": False,
                    "enableValue": False,
                    "enablePivot": False,
                    'cellStyle': {'white-space': 'pre',
                                  'display': 'grid',
                                  'text-align': 'center',
                                  'align-items': 'center',
                                  },
                    # "tooltipComponent": "CustomTooltip"
                    },
    columnSize="sizeToFit", 
    getRowId='params.data.index', 
    style={ "width": "100%",
           'height':f'{45.5 *20}px'
           }
)