import pandas as pd


def __netsplit(edges, outcome_idx, net_split_data, consistency_data):
    df = (pd.read_json(net_split_data[0], orient='split') if not outcome_idx
          else  pd.read_json(net_split_data[outcome_idx], orient='split'))
    consistency_data = pd.read_json(consistency_data[0], orient='split')

    if df is not None:
        comparisons = df.comparison.str.split(':', expand=True)
        df['Comparison'] = comparisons[0] + ' vs ' + comparisons[1]
        df = df.loc[:, ~df.columns.str.contains("comparison")]
        df = df.sort_values(by='Comparison').reset_index()
        df = df[['Comparison', "direct", "indirect", "p-value"]].round(decimals=3)
        # df["direct"] = df["direct"].round(2)
        # df["indirect"] = df["indirect"].round(2)

    slctd_comps = []
    for edge in edges or []:
        src, trgt = edge['source'], edge['target']
        # slctd_comps += [f'{src} vs {trgt}']
        slctd_comps += [f'{src} vs {trgt}', f'{trgt} vs {src}']

    if edges and df is not None:
        df = df[df.Comparison.isin(slctd_comps)]

    data_cols = [{"name": c, "id": c} for c in df.columns]
    data_output = df.to_dict('records') if df is not None else dict()
    _out_net_split_table = [data_output, data_cols]

    consistency_data['Q'] = consistency_data['Q'].round(2)
    consistency_data['p-value'] = consistency_data['p-value'].round(3)
    data_consistency = consistency_data.to_dict('records')
    consistency_tbl_cols = [{"name": i, "id": i} for i in consistency_data.columns]
    if data_consistency[0]['p-value'] == 0.0: data_consistency[0]['p-value'] = '<0.0001'

    _out_consistency_table = [data_consistency, consistency_tbl_cols]


    return _out_net_split_table + _out_consistency_table