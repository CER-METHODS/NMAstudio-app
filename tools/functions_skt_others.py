import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

def get_skt_elements():
    df = pd.read_csv('db/psoriasis_wide_complete.csv')
    num_classes = None
    i=0
    df = df.dropna(subset=[f'TE{i+1}', f'seTE{i+1}'])
    if "treat1_class" and "treat2_class" in df.columns:
        df_treat = df.treat1.dropna().append(df.treat2.dropna()).reset_index(drop=True)
        df_class = df.treat1_class.dropna().append(df.treat2_class.dropna()).reset_index(drop=True)
        long_df_class = pd.concat([df_treat,df_class], axis=1).reset_index(drop=True)
        long_df_class = long_df_class.rename({long_df_class.columns[0]: 'treat', long_df_class.columns[1]: 'class'}, axis='columns')
        if not is_numeric_dtype(long_df_class.columns[1]):
            long_df_class["class_codes"] = long_df_class['class'].astype("category").cat.codes
            long_df_class = long_df_class.rename({long_df_class.columns[0]: 'treat', long_df_class.columns[1]: 'class_names',
                                                  long_df_class.columns[2]: 'class'},
                                                  axis='columns')
        all_nodes_class = long_df_class.drop_duplicates().sort_values(by='treat').reset_index(drop=True)
        num_classes = all_nodes_class['class'].max()+1 
    sorted_edges = np.sort(df[['treat1', 'treat2']], axis=1)  ## removes directionality
    df.loc[:,['treat1', 'treat2']] = sorted_edges  
    edges = df.groupby(['treat1', 'treat2'])[f"TE{i+1}"].count().reset_index()
    df_n1g = df.rename(columns={'treat1': 'treat', f'n1{i+1}': 'n'}).groupby(['treat'])
    df_n2g = df.rename(columns={'treat2': 'treat', f'n2{i+1}': 'n'}).groupby(['treat'])
    df_n1, df_n2 = df_n1g.n.sum(), df_n2g.n.sum()
    all_nodes_sized = df_n1.add(df_n2, fill_value=0)
    df_n1, df_n2 = df_n1g.rob.value_counts(), df_n2g.rob.value_counts()
    all_nodes_robs = df_n1.add(df_n2, fill_value=0).rename(('count')).unstack('rob', fill_value=0)
    all_nodes_sized = pd.concat([all_nodes_sized, all_nodes_robs], axis=1).reset_index()


    if isinstance(all_nodes_sized.columns[2], str):
        for c in {'1', '2', '3'}.difference(all_nodes_sized): all_nodes_sized[c] = 0
    elif all_nodes_sized.columns[2] in {1, 2, 3}:
        for c in {1, 2, 3}.difference(all_nodes_sized): all_nodes_sized[c] = 0
    elif all_nodes_sized.columns[2] in {1.0, 2.0, 3.0}:
        for c in {1.0, 2.0, 3.0}.difference(all_nodes_sized): all_nodes_sized[c] = 0

    all_nodes_robs.drop(columns=[col for col in all_nodes_robs if col not in [1.0, 2.0, 3.0, 1, 2, 3, '1','2','3']], inplace=True)
    all_nodes_sized.drop(columns=[col for col in all_nodes_sized if col not in ['treat', 'n', 'class', 1.0, 2.0, 3.0, 1, 2, 3, '1','2','3']], inplace=True)
    # all_nodes_sized['n_2'] = all_nodes_sized['n']
    min_size = min(all_nodes_sized['n'])
    max_size = max(all_nodes_sized['n'])

    # Calculate the range of 'size'
    size_range = max_size - min_size

    # Normalize the values in 'size' to the range of 10 to 60
    normalized_size = [(s - min_size) / size_range for s in all_nodes_sized.n]
    number = [int(n * 60) + 20 for n in normalized_size]
    all_nodes_sized['n_2']=number

    cy_edges = [{'data': {'source': source, 'target': target,
                          'weight': weight * 1 if (len(edges)<100 and len(edges)>13) else weight * 0.75 if len(edges)<13  else weight * 0.7,
                          'weight_lab': weight}}
                for source, target, weight in edges.values]
    # max_trsfrmd_size_nodes = np.sqrt(all_nodes_sized.iloc[:,1].max()) / 70
    # node_size = float(node_size) if node_size is not None else 0

   
    cy_nodes = [{"data": {"id": target,
                            "label": target,
                            'classes': 'genesis',
                            'size': n2,
                        #   'size': np.power(size,1/4)*8 /( max_trsfrmd_size_nodes-node_size),
                            'pie1': r1 / (r1 + r2 + r3) if not r1 + r2 + r3 == 0 else None,
                            'pie2': r2 / (r1 + r2 + r3) if not r1 + r2 + r3 == 0 else None,
                            'pie3': r3 / (r1 + r2 + r3) if not r1 + r2 + r3 == 0 else None},
                            } for
                target, size, r1, r2, r3,n2 in all_nodes_sized.values]

    return cy_edges + cy_nodes




def skt_stylesheet(node_size=False, classes=False, edg_col= 'grey', nd_col='#07ABA0', edge_size=False,
                   pie=False, edg_lbl=False, nodes_opacity=1, edges_opacity=0.77,label_size=False):
    cmaps_class = ['#07ABA0']
    default_stylesheet = [
        {"selector": 'node',
         'style': {"opacity": nodes_opacity,
                   'background-color': nd_col,
                   'node-text-rotation': 'autorotate',
                   'line-color':'black',
                   'label': "data(label)",
                   'shape':'circle',
                   'color': "black", #"#1b242b"
                   'font-size': label_size,
                   'width':25,
                   'height':25
                #    'position':'data(position)'

                   },
         },
        {"selector": 'edge',
         'style': {"curve-style": "bezier",
                   'width': 'data(weight)',
                   'line-color': edg_col,
                    "opacity": edges_opacity}}]
   

    if classes:
       # default_stylesheet[0]['style'].update({"shape": "triangle"})
       list_classes = [{'selector': '.' + f'{x}',
                        'style': {'background-color': f'{x}',
                                  }} for x in cmaps_class]
       for x in list_classes:
           default_stylesheet.append(x)
    # if node_size: default_stylesheet[0]['style'].update({"width": "data(size)", "height": "data(size)"})
    if node_size: default_stylesheet[0]['style'].update({"width": "data(size)", "height": "data(size)"})
    if edge_size: default_stylesheet[1]['style'].update({"width": None})
    # if edg_col:   default_stylesheet[1]['style'].update({'line-color': edg_col})
    if edg_lbl:   default_stylesheet[1]['style'].update({'label': 'data(weight_lab)'})
    if pie:       default_stylesheet[0]['style'].update({
                                               'pie-1-background-color': '#E8747C',
                                               'pie-1-background-size': 'mapData(pie3, 0, 1, 0, 100)',
                                               'pie-2-background-color': '#f8d49d', #'#74CBE8',
                                               'pie-2-background-size': 'mapData(pie2, 0, 1, 0, 100)',
                                               'pie-3-background-color': '#5aa469',
                                               'pie-3-background-size': 'mapData(pie1, 0, 1, 0, 100)',
         })
    return default_stylesheet