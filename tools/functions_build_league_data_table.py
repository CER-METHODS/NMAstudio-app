import numpy as np, pandas as pd
import dash, dash_html_components as html
import dash_table
from tools.utils import set_slider_marks
from assets.COLORS import *

# def __update_output(store_node, net_data, store_edge, toggle_cinema, toggle_cinema_modal, slider_value,
#                    league_table_data, cinema_net_data1, cinema_net_data2, data_and_league_table_DATA,
#                    forest_data, forest_data_out2, reset_btn, ranking_data, net_storage, net_data_STORAGE_TIMESTAMP,
#                    data_filename, league_table_data_STORAGE_TIMESTAMP, filename_cinema1, filename_cinema2,  filename_cinema2_disabled):


#     YEARS_DEFAULT = np.array([1963, 1990, 1997, 2001, 2003, 2004, 2005, 2006, 2007, 2008, 2010,
#                               2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])

#     reset_btn_triggered = False
#     triggered = [tr['prop_id'] for tr in dash.callback_context.triggered]
#     if 'reset_project.n_clicks' in triggered: reset_btn_triggered = True

#     net_data = pd.read_json(net_data, orient='split').round(3)

#     years = net_data.year #if (not reset_btn_triggered) else YEARS_DEFAULT
#     slider_min, slider_max = years.min(), years.max()
#     slider_marks = set_slider_marks(slider_min, slider_max, years)
#     _out_slider = [slider_min, slider_max, slider_marks]


#     triggered = [tr['prop_id'] for tr in dash.callback_context.triggered]
#     if 'rob_vs_cinema.value' in triggered: toggle_cinema_modal = toggle_cinema
#     elif 'rob_vs_cinema_modal.value' in triggered: toggle_cinema = toggle_cinema_modal

#     if 'slider-year.value' in triggered:
#         _data = pd.read_json(data_and_league_table_DATA['FULL_DATA'], orient='split').round(3)
#         data_output = _data[_data.year <= slider_value].to_dict('records')
#         _OUTPUT0 = data_and_league_table_DATA['OUTPUT']
#         _output = [data_output] + [_OUTPUT0[1]] + [data_output] + _OUTPUT0[3: ]
#         return _output + _out_slider + [data_and_league_table_DATA]


#     ranking_data = pd.read_json(ranking_data, orient='split')
#     leaguetable = pd.read_json(league_table_data, orient='split')
#     confidence_map = {k : n for n, k in enumerate(['low', 'medium', 'high'])}
#     treatments = np.unique(net_data[['treat1', 'treat2']].dropna().values.flatten())


#     net_data['rob'] = net_data['rob'].replace('__none__', '')
#     net_data['rob'] = net_data['rob'].replace('.', np.nan)
#     net_data['rob'] = net_data['rob'].replace('', np.nan)
#     #net_data['rob'] = net_data['rob'].astype(int)

#     robs = (net_data.groupby(['treat1', 'treat2']).rob.mean().reset_index()
#             .pivot_table(index='treat2', columns='treat1', values='rob')
#             .reindex(index=treatments, columns=treatments, fill_value=np.nan))


#     robs = robs.fillna(robs.T) if not toggle_cinema else robs
#     robs_slct = robs #robs + robs.T - np.diag(np.diag(robs))  if not toggle_cinema else robs ## full rob table

#     comprs_downgrade  = pd.DataFrame()
#     comprs_conf_lt = comprs_conf_ut = None
 




#     if toggle_cinema:

#         cinema_net_data1 = pd.read_json(cinema_net_data1, orient='split')
#         cinema_net_data2 = pd.read_json(cinema_net_data2, orient='split')
#         confidence_map = {k : n for n, k in enumerate(['very low', 'low', 'moderate', 'high'])}
#         comparisons1 = cinema_net_data1.Comparison.str.split(':', expand=True)
#         confidence1 = cinema_net_data1['Confidence rating'].str.lower().map(confidence_map)
#         if filename_cinema2 is not None or (filename_cinema2 is None and "Default_data" in cinema_net_data2.columns):
#             confidence2 = cinema_net_data2['Confidence rating'].str.lower().map(confidence_map)
#         else:
#             confidence2 = pd.Series(np.array([np.nan]*len(confidence1)), copy=False)
#         comparisons2 = cinema_net_data2.Comparison.str.split(':', expand=True) if filename_cinema2 is not None or (filename_cinema2 is None and "Default_data" not in cinema_net_data2.columns) else comparisons1
#         comprs_conf_ut = comparisons2.copy()  # Upper triangle
#         comparisons1.columns = [1, 0]  # To get lower triangle
#         comprs_conf_lt = comparisons1  # Lower triangle
#         comprs_downgrade_lt = comprs_conf_lt
#         comprs_downgrade_ut = comprs_conf_ut
#         if "Reason(s) for downgrading" in cinema_net_data1.columns:
#             downgrading1 = cinema_net_data1["Reason(s) for downgrading"]
#             comprs_downgrade_lt['Downgrading'] = downgrading1
#             if (filename_cinema2 is not None) or (filename_cinema2 is None and "Default_data" in cinema_net_data2.columns) and ("Reason(s) for downgrading" in cinema_net_data2.columns):
#                 downgrading2 = cinema_net_data2["Reason(s) for downgrading"]
#             else:
#                 downgrading2 = pd.Series(np.array([np.nan]*len(downgrading1)), copy=False)
#             comprs_downgrade_ut['Downgrading'] = downgrading2
#             comprs_downgrade = pd.concat([comprs_downgrade_ut, comprs_downgrade_lt])
#             comprs_downgrade = comprs_downgrade.pivot(index=0, columns=1, values='Downgrading')
#         comprs_conf_lt['Confidence'] = confidence1
#         comprs_conf_ut['Confidence'] = confidence2
#         comprs_conf = pd.concat([comprs_conf_ut, comprs_conf_lt])
#         comprs_conf = comprs_conf.pivot_table(index=0, columns=1, values='Confidence')

#         if filename_cinema2 is None and "pscore2" not in ranking_data.columns:
#             ut = np.triu(np.ones(comprs_conf.shape), 1).astype(bool)
#             comprs_conf = comprs_conf.where(ut == False, np.nan)

#         robs = comprs_conf
#     # Filter according to cytoscape selection

#     if store_node:
#         slctd_trmnts = [nd['id'] for nd in store_node]
#         if len(slctd_trmnts) > 0:
#             forest_data = pd.read_json(forest_data, orient='split')
#             net_data = pd.read_json(net_storage, orient='split')
#             forest_data_out2 = pd.read_json(forest_data_out2, orient='split') if 'pscore2' in ranking_data.columns else None
#             dataselectors = []
#             dataselectors += [forest_data.columns[1], net_data["outcome1_direction"].iloc[1]]
#             if 'pscore2' in ranking_data.columns:
#                 dataselectors += [forest_data_out2.columns[1], net_data["outcome2_direction"].iloc[1]]

#             leaguetable = leaguetable.loc[slctd_trmnts, slctd_trmnts]
#             robs_slct = robs.loc[slctd_trmnts, slctd_trmnts]
#             leaguetable_bool = pd.DataFrame(np.triu(np.ones(leaguetable.shape)).astype(bool),
#                                             columns=slctd_trmnts,
#                                             index=slctd_trmnts) #define upper and lower triangle

#             ### pick correct comparison from FOREST_DATA and FOREST_DATA_OUT2
#             for treat_c in slctd_trmnts:
#                 for treat_r in slctd_trmnts:
#                     if treat_c != treat_r:
#                         if not leaguetable_bool.loc[treat_r][treat_c]:
#                             effcsze = round(forest_data[dataselectors[0]][(forest_data.Treatment == treat_c) & (forest_data.Reference == treat_r)].values[0], 2)
#                             ci_lower = round(forest_data['CI_lower'][(forest_data.Treatment == treat_c) & (forest_data.Reference == treat_r)].values[0], 2)
#                             ci_upper = round(forest_data['CI_upper'][(forest_data.Treatment == treat_c) & (forest_data.Reference == treat_r)].values[0], 2)
#                             leaguetable.loc[treat_r][treat_c] = f'{effcsze}\n{ci_lower, ci_upper}'
#                         else:
#                             pass
#                             #direct = round(float(leaguetable.loc[treat_r][treat_c].strip().split("\n")[0]), 2) if leaguetable[treat_r][treat_c] != "." else None
#                             #leaguetable.loc[treat_r][treat_c] = np.exp( -np.log(direct)) if leaguetable[treat_r][treat_c] != "." else  "." # TODO: might want to save direct evidence from R and update it upoon filtering, so far it is removed iif nodes are filtered
#                             # leaguetable = pd.DataFrame(np.tril(leaguetable), columns=slctd_trmnts, index=slctd_trmnts)
#                         if 'pscore2' in ranking_data.columns:
#                             effcsze2 = round(forest_data_out2[dataselectors[2]][(forest_data_out2.Treatment == treat_r) & (forest_data_out2.Reference == treat_c)].values[0], 2)
#                             ci_lower2 = round(forest_data_out2['CI_lower'][(forest_data_out2.Treatment == treat_r) & (forest_data_out2.Reference == treat_c)].values[0], 2)
#                             ci_upper2 = round(forest_data_out2['CI_upper'][(forest_data_out2.Treatment == treat_r) & (forest_data_out2.Reference == treat_c)].values[0], 2)

#                             if leaguetable_bool.loc[treat_r][treat_c]:
#                                 leaguetable.loc[treat_r][treat_c] = f'{effcsze2}\n{ci_lower2, ci_upper2}'
#                                 if toggle_cinema: robs_slct.loc[treat_r][treat_c] = comprs_conf_ut['Confidence'][(comprs_conf_ut[0] == treat_c) & (comprs_conf_ut[1] == treat_r) |
#                                                                                     (comprs_conf_ut[0] == treat_r) & (comprs_conf_ut[1] == treat_c)].values[0]
#                                 else:
#                                     robs_slct.loc[treat_r][treat_c] = robs_slct[treat_r][treat_c] if not np.isnan(robs_slct[treat_r][treat_c]) else robs_slct[treat_c][treat_r]

#                             else:
#                                 if toggle_cinema: robs_slct.loc[treat_r][treat_c] = comprs_conf_lt['Confidence'][(comprs_conf_lt[0] == treat_c) & (comprs_conf_lt[1] == treat_r) |
#                                                                                     (comprs_conf_lt[0] == treat_r) & (comprs_conf_lt[1] == treat_c)].values[0]
#                                 else:
#                                     robs_slct.loc[treat_r][treat_c] = robs_slct[treat_r][treat_c] if not np.isnan(robs_slct[treat_r][treat_c]) else robs_slct[treat_c][treat_r]
#                         else:
#                             if toggle_cinema:
#                                 robs_slct.loc[treat_r][treat_c] = comprs_conf_lt['Confidence'][
#                                     (comprs_conf_lt[0] == treat_c) & (comprs_conf_lt[1] == treat_r) |
#                                     (comprs_conf_lt[0] == treat_r) & (comprs_conf_lt[1] == treat_c)].values[0]
#                             else:
#                                 robs_slct.loc[treat_r][treat_c] = robs_slct[treat_r][treat_c] if not np.isnan(
#                                     robs_slct[treat_r][treat_c]) else robs_slct[treat_c][treat_r]

#             if 'pscore2' not in ranking_data.columns:
#                 if not toggle_cinema:
#                     robs_slct = robs_slct[leaguetable_bool.T]
#                     leaguetable = leaguetable[leaguetable_bool.T]
#                 else:
#                     robs_slct = robs_slct[leaguetable_bool.T]
#                     leaguetable = leaguetable[leaguetable_bool.T]


#             leaguetable.replace(0, np.nan) #inplace

#             tril_order = pd.DataFrame(np.tril(np.ones(leaguetable.shape)),
#                                       columns=leaguetable.columns,
#                                       index=leaguetable.columns)
#             tril_order = tril_order.loc[slctd_trmnts, slctd_trmnts]
#             filter = np.tril(tril_order == 0)
#             filter += filter.T  # inverting of rows and columns common in meta-analysis visualissation

#             robs = robs.loc[slctd_trmnts, slctd_trmnts]
#             robs_values = robs.values
#             #robs_values[filter] = robs_values.T[filter]
#             robs = pd.DataFrame(robs_values,
#                                 columns=robs.columns,
#                                 index=robs.columns)

#             robs = robs.T if 'pscore2' not in ranking_data.columns else robs

#             treatments = slctd_trmnts

#     #####   Add style colouring and legend
#     N_BINS = 3 if not toggle_cinema else 4
#     bounds = np.arange(N_BINS + 1) / N_BINS
#     leaguetable_colr = robs.copy(deep=True)
#     np.fill_diagonal(leaguetable_colr.values, np.nan)
#     leaguetable_colr = leaguetable_colr.astype(np.float64)

#     cmap = [CINEMA_g, CINEMA_y, CINEMA_r] if not toggle_cinema else [CINEMA_r, CINEMA_y, CINEMA_lb, CINEMA_g]
#     legend_height = '4px'
#     legend = [html.Div(style={'display': 'inline-block', 'width': '100px'},
#                        children=[html.Div(),
#                                  html.Small('Risk of bias: ' if not toggle_cinema else 'CINeMA rating: ',
#                                             style={'color': 'black'})])]
#     legend += [html.Div(style={'display': 'inline-block', 'width': '60px'},
#                         children=[html.Div(style={'backgroundColor': cmap[n],
#                                                   'height': legend_height}), html.Small(
#                             ('Very Low' if toggle_cinema else 'Low') if n == 0 else 'High' if n == N_BINS - 1 else None,
#                             style={'paddingLeft': '2px', 'color': 'black'})])
#                for n in range(N_BINS)]

#     cmap = [CINEMA_g, CINEMA_y, CINEMA_r] if not toggle_cinema else [CINEMA_r, CINEMA_y, CINEMA_lb, CINEMA_g]

#     df_max, df_min = max(confidence_map.values()), min(confidence_map.values())
#     ranges = (df_max - df_min) * bounds + df_min
#     ranges[-1] *= 1.001
#     ranges = ranges + 1 if not toggle_cinema else ranges
#     league_table_styles = []


#     for treat_c in treatments:
#         for treat_r in treatments:
#             if treat_r!=treat_c:

#                 rob = robs.loc[treat_r, treat_c] if not store_node else robs_slct.loc[treat_r, treat_c]
#                 indxs = np.where(rob < ranges)[0] if rob == rob else [0]
#                 clr_indx = indxs[0] - 1 if len(indxs) else 0
#                 diag, empty = treat_r == treat_c, rob != rob
#                 league_table_styles.append({'if': {'filter_query': f'{{Treatment}} = {{{treat_r}}}',
#                                                 'column_id': treat_c},
#                                                 'backgroundColor': cmap[clr_indx] if not empty else CLR_BCKGRND2,
#                                                 'color': 'white' if not empty else CX2 if diag else 'black'})
#     league_table_styles.append({'if': {'column_id': 'Treatment'}, 'backgroundColor': CX1})



#     # Prepare for output
#     tips = robs

#     leaguetable = leaguetable.reset_index().rename(columns={'index': 'Treatment'})
#     leaguetable_cols = [{"name": c, "id": c} for c in leaguetable.columns]
#     leaguetable = leaguetable.to_dict('records')

#     tooltip_values = [{col['id']: {'value': f"**Average ROB:** {tip[col['id']]}",
#                                    'type': 'markdown'} if col['id'] != 'Treatment' else None
#                            for col in leaguetable_cols} for rn, (_, tip) in enumerate(tips.iterrows())]
#     if toggle_cinema:
#         tooltip_values = [{col['id']: {'value': f"**Reason for Downgrading:**{tip[col['id']]}" if not comprs_downgrade.empty and not store_node else f"**Reason for Downgrading:**",
#                                        'type': 'markdown'} if col['id'] != 'Treatment' else None
#                        for col in leaguetable_cols} for rn, (_, tip) in enumerate(comprs_downgrade.iterrows())]


#     if store_edge or store_node:
#         slctd_nods = {n['id'] for n in store_node} if store_node else set()
#         slctd_edgs = [e['source'] + e['target'] for e in store_edge] if store_edge else []
#         net_data = net_data[net_data.treat1.isin(slctd_nods) | net_data.treat2.isin(slctd_nods)
#                     | (net_data.treat1 + net_data.treat2).isin(slctd_edgs) | (net_data.treat2 + net_data.treat1).isin(slctd_edgs)]


#     data_cols = [{"name": c, "id": c} for c in net_data.columns]
#     data_output = net_data[net_data.year <= slider_value].to_dict('records')
#     league_table = build_league_table(leaguetable, leaguetable_cols, league_table_styles, tooltip_values)
#     league_table_modal = build_league_table(leaguetable, leaguetable_cols, league_table_styles, tooltip_values, modal=True)
#     _output = [data_output, data_cols] * 2 + [league_table, league_table_modal] + [legend] * 2 + [toggle_cinema, toggle_cinema_modal]

#     data_and_league_table_DATA['FULL_DATA'] = net_data.to_json( orient='split')
#     data_and_league_table_DATA['OUTPUT'] = _output

#     return  _output + _out_slider + [data_and_league_table_DATA]


# def __update_output_new(store_node, net_data, store_edge,slider_value,reset_btn, data_and_league_table_DATA, 
#                         net_storage, net_data_STORAGE_TIMESTAMP,
#                   data_filename, league_table_data_STORAGE_TIMESTAMP, filename_cinema1):


#     YEARS_DEFAULT = np.array([1963, 1990, 1997, 2001, 2003, 2004, 2005, 2006, 2007, 2008, 2010,
#                               2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])

#     reset_btn_triggered = False
#     triggered = [tr['prop_id'] for tr in dash.callback_context.triggered]
#     if 'reset_project.n_clicks' in triggered: reset_btn_triggered = True
#     # net_data = net_data[0]
#     # df = pd.read_json(net_data[0], orient='split')
#     net_data = pd.read_json(net_data[0], orient='split').round(3)

#     years = net_data.year #if (not reset_btn_triggered) else YEARS_DEFAULT
#     slider_min, slider_max = years.min(), years.max()
#     slider_marks = set_slider_marks(slider_min, slider_max, years)
#     _out_slider = [slider_min, slider_max, slider_marks]


#     triggered = [tr['prop_id'] for tr in dash.callback_context.triggered]

#     # if 'slider-year.value' in triggered:
#     #     _data = pd.read_json(data_and_league_table_DATA['FULL_DATA'], orient='split').round(3)
#     #     data_output = _data[_data.year <= slider_value].to_dict('records')
#     #     _OUTPUT0 = data_and_league_table_DATA['OUTPUT']
#     #     _output = [data_output, _OUTPUT0[1]]*2
#     #     return _output + _out_slider + [data_and_league_table_DATA]
        


#     # net_data['rob'] = net_data['rob'].replace('__none__', '')
#     # net_data['rob'] = net_data['rob'].replace('.', np.nan)
#     # net_data['rob'] = net_data['rob'].replace('', np.nan)



#     if store_edge or store_node:
#         slctd_nods = {n['id'] for n in store_node} if store_node else set()
#         slctd_edgs = [e['source'] + e['target'] for e in store_edge] if store_edge else []
#         net_data = net_data[net_data.treat1.isin(slctd_nods) | net_data.treat2.isin(slctd_nods)
#                     | (net_data.treat1 + net_data.treat2).isin(slctd_edgs) | (net_data.treat2 + net_data.treat1).isin(slctd_edgs)]

#     net_data2 = net_data.copy()
#     data_cols = [{"name": c, "id": c} for c in net_data2.columns]
#     data_output = net_data2.to_dict('records')
#     # data_output = net_data[net_data.year <= slider_value].to_dict('records')
#     _output = [data_output, data_cols] * 2
#     data_and_league_table_DATA['FULL_DATA'] = net_data2.to_json( orient='split')
#     data_and_league_table_DATA['OUTPUT'] = _output

#     return [data_output, data_cols] * 2 + _out_slider + [data_and_league_table_DATA]




def __update_output_new(slider_value, store_node,store_edge,net_data,raw_data, toggle_cinema, toggle_cinema_modal,
                  league_table_data, cinema_net_data, data_and_league_table_DATA,
                  forest_data,  reset_btn,  outcome_idx, net_storage, raw_storage):
    # if outcome_idx:
    #     outcome_idx = outcome_idx
    # else:
    #     outcome_idx = 0

    YEARS_DEFAULT = np.array([1963, 1990, 1997, 2001, 2003, 2004, 2005, 2006, 2007, 2008, 2010,
                              2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])

    reset_btn_triggered = False
    triggered = [tr['prop_id'] for tr in dash.callback_context.triggered]
    if 'reset_project.n_clicks' in triggered: reset_btn_triggered = True

    net_data = pd.read_json(net_data[0], orient='split').round(3)
    raw_data = pd.read_json(raw_data[0], orient='split').round(3)

    years = net_data.year #if (not reset_btn_triggered) else YEARS_DEFAULT
    slider_min, slider_max = years.min(), years.max()
    slider_marks = set_slider_marks(slider_min, slider_max, years)
    _out_slider = [slider_min, slider_max, slider_marks]




    triggered = [tr['prop_id'] for tr in dash.callback_context.triggered]
    if 'rob_vs_cinema.value' in triggered: toggle_cinema_modal = toggle_cinema
    elif 'rob_vs_cinema_modal.value' in triggered: toggle_cinema = toggle_cinema_modal

    if 'slider-year.value' in triggered:
        _data = pd.read_json(data_and_league_table_DATA['FULL_DATA'], orient='split').round(3)
        data_output = _data[_data.year <= slider_value].to_dict('records')
        _OUTPUT0 = data_and_league_table_DATA['OUTPUT']
        _output = [data_output] + [_OUTPUT0[1]] + [data_output] + _OUTPUT0[3: ]
        return _output + _out_slider + [data_and_league_table_DATA]



    # ranking_data = pd.read_json(ranking_data, orient='split')
    leaguetable = pd.read_json(league_table_data[outcome_idx], orient='split')
    confidence_map = {k : n for n, k in enumerate(['low', 'medium', 'high'])}
    treatments = np.unique(net_data[['treat1', 'treat2']].dropna().values.flatten())


    net_data['rob'] = net_data['rob'].replace('__none__', '')
    net_data['rob'] = net_data['rob'].replace('.', np.nan)
    net_data['rob'] = net_data['rob'].replace('', np.nan)
    #net_data['rob'] = net_data['rob'].astype(int)

    robs = (net_data.groupby(['treat1', 'treat2']).rob.mean().reset_index()
            .pivot_table(index='treat2', columns='treat1', values='rob')
            .reindex(index=treatments, columns=treatments, fill_value=np.nan))


    robs = robs.fillna(robs.T) if not toggle_cinema else robs
    robs_slct = robs #robs + robs.T - np.diag(np.diag(robs))  if not toggle_cinema else robs ## full rob table

    comprs_downgrade  = pd.DataFrame()
    comprs_conf_lt = comprs_conf_ut = None
    
    if store_edge or store_node:
        slctd_nods = {n['id'] for n in store_node} if store_node else set()
        slctd_edgs = [e['source'] + e['target'] for e in store_edge] if store_edge else []
        net_data = net_data[net_data.treat1.isin(slctd_nods) | net_data.treat2.isin(slctd_nods)
                    | (net_data.treat1 + net_data.treat2).isin(slctd_edgs) | (net_data.treat2 + net_data.treat1).isin(slctd_edgs)]


    if toggle_cinema:
        # print(cinema_net_data)
        cinema_net_data = pd.read_json(cinema_net_data[outcome_idx], orient='split')
        # cinema_net_data2 = pd.read_json(cinema_net_data2[0], orient='split')
        confidence_map = {k : n for n, k in enumerate(['very low', 'low', 'moderate', 'high'])}
        comparisons1 = cinema_net_data.Comparison.str.split(':', expand=True)
        confidence1 = cinema_net_data['Confidence rating'].str.lower().map(confidence_map)

        confidence2 = pd.Series(np.array([np.nan]*len(confidence1)), copy=False)
        comparisons2 = comparisons1
        comprs_conf_ut = comparisons2.copy()  # Upper triangle
        comparisons1.columns = [1, 0]  # To get lower triangle
        comprs_conf_lt = comparisons1  # Lower triangle
        comprs_downgrade_lt = comprs_conf_lt
        comprs_downgrade_ut = comprs_conf_ut
        if "Reason(s) for downgrading" in cinema_net_data.columns:
            downgrading1 = cinema_net_data["Reason(s) for downgrading"]
            comprs_downgrade_lt['Downgrading'] = downgrading1

            downgrading2 = pd.Series(np.array([np.nan]*len(downgrading1)), copy=False)
            comprs_downgrade_ut['Downgrading'] = downgrading2
            comprs_downgrade = pd.concat([comprs_downgrade_ut, comprs_downgrade_lt])
            comprs_downgrade = comprs_downgrade.pivot(index=0, columns=1, values='Downgrading')
        comprs_conf_lt['Confidence'] = confidence1
        comprs_conf_ut['Confidence'] = confidence2
        comprs_conf = pd.concat([comprs_conf_ut, comprs_conf_lt])
        comprs_conf = comprs_conf.pivot(index=0, columns=1, values='Confidence')

        ut = np.triu(np.ones(comprs_conf.shape), 1).astype(bool)
        comprs_conf = comprs_conf.where(ut == False, np.nan)

        robs = comprs_conf
    # Filter according to cytoscape selection

    if store_node and any('id' in nd for nd in store_node):
        slctd_trmnts = [nd['id'] for nd in store_node]
        if len(slctd_trmnts) > 0:
            forest_data = pd.read_json(forest_data[outcome_idx], orient='split')
            net_data = pd.read_json(net_storage[0], orient='split')
            # forest_data_out2 =  None
            dataselectors = []
            dataselectors += [forest_data.columns[1], net_data["outcome1_direction"].iloc[1]]
            # if 'pscore2' in ranking_data.columns:
            #     dataselectors += [forest_data_out2.columns[1], net_data["outcome2_direction"].iloc[1]]

            leaguetable = leaguetable.loc[slctd_trmnts, slctd_trmnts]
            robs_slct = robs.loc[slctd_trmnts, slctd_trmnts]
            leaguetable_bool = pd.DataFrame(np.triu(np.ones(leaguetable.shape)).astype(bool),
                                            columns=slctd_trmnts,
                                            index=slctd_trmnts) #define upper and lower triangle

            ### pick correct comparison from FOREST_DATA and FOREST_DATA_OUT2
            for treat_c in slctd_trmnts:
                for treat_r in slctd_trmnts:
                    if treat_c != treat_r:
                        if not leaguetable_bool.loc[treat_r][treat_c]:
                            effcsze = round(forest_data[dataselectors[0]][(forest_data.Treatment == treat_c) & (forest_data.Reference == treat_r)].values[0], 2)
                            ci_lower = round(forest_data['CI_lower'][(forest_data.Treatment == treat_c) & (forest_data.Reference == treat_r)].values[0], 2)
                            ci_upper = round(forest_data['CI_upper'][(forest_data.Treatment == treat_c) & (forest_data.Reference == treat_r)].values[0], 2)
                            leaguetable.loc[treat_r][treat_c] = f'{effcsze}\n{ci_lower, ci_upper}'
                        else:
                            pass

                        if toggle_cinema:
                            robs_slct.loc[treat_r][treat_c] = comprs_conf_lt['Confidence'][
                                (comprs_conf_lt[0] == treat_c) & (comprs_conf_lt[1] == treat_r) |
                                (comprs_conf_lt[0] == treat_r) & (comprs_conf_lt[1] == treat_c)].values[0]
                        else:
                            robs_slct.loc[treat_r][treat_c] = robs_slct[treat_r][treat_c] if not np.isnan(
                                robs_slct[treat_r][treat_c]) else robs_slct[treat_c][treat_r]

            
            if not toggle_cinema:
                robs_slct = robs_slct[leaguetable_bool.T]
                leaguetable = leaguetable[leaguetable_bool.T]
            else:
                robs_slct = robs_slct[leaguetable_bool.T]
                leaguetable = leaguetable[leaguetable_bool.T]


            leaguetable.replace(0, np.nan) #inplace

            tril_order = pd.DataFrame(np.tril(np.ones(leaguetable.shape)),
                                      columns=leaguetable.columns,
                                      index=leaguetable.columns)
            tril_order = tril_order.loc[slctd_trmnts, slctd_trmnts]
            filter = np.tril(tril_order == 0)
            filter += filter.T  # inverting of rows and columns common in meta-analysis visualissation

            robs = robs.loc[slctd_trmnts, slctd_trmnts]
            robs_values = robs.values
            #robs_values[filter] = robs_values.T[filter]
            robs = pd.DataFrame(robs_values,
                                columns=robs.columns,
                                index=robs.columns)

            

            treatments = slctd_trmnts

    #####   Add style colouring and legend
    N_BINS = 3 if not toggle_cinema else 4
    bounds = np.arange(N_BINS + 1) / N_BINS
    leaguetable_colr = robs.copy(deep=True)
    np.fill_diagonal(leaguetable_colr.values, np.nan)
    leaguetable_colr = leaguetable_colr.astype(np.float64)

    cmap = [CINEMA_g, CINEMA_y, CINEMA_r] if not toggle_cinema else [CINEMA_r, CINEMA_y, CINEMA_lb, CINEMA_g]
    legend_height = '4px'
    legend = [html.Div(style={'display': 'inline-block', 'width': '100px'},
                       children=[html.Div(),
                                 html.Small('Risk of bias: ' if not toggle_cinema else 'CINeMA rating: ',
                                            style={'color': 'black'})])]
    legend += [html.Div(style={'display': 'inline-block', 'width': '60px'},
                        children=[html.Div(style={'backgroundColor': cmap[n],
                                                  'height': legend_height}), html.Small(
                            ('Very Low' if toggle_cinema else 'Low') if n == 0 else 'High' if n == N_BINS - 1 else None,
                            style={'paddingLeft': '2px', 'color': 'black'})])
               for n in range(N_BINS)]

    cmap = [CINEMA_g, CINEMA_y, CINEMA_r] if not toggle_cinema else [CINEMA_r, CINEMA_y, CINEMA_lb, CINEMA_g]

    df_max, df_min = max(confidence_map.values()), min(confidence_map.values())
    ranges = (df_max - df_min) * bounds + df_min
    ranges[-1] *= 1.001
    ranges = ranges + 1 if not toggle_cinema else ranges
    league_table_styles = []


    for treat_c in treatments:
        for treat_r in treatments:
            if treat_r!=treat_c:

                rob = robs.loc[treat_r, treat_c] if not store_node else robs_slct.loc[treat_r, treat_c]
                indxs = np.where(rob < ranges)[0] if rob == rob else [0]
                clr_indx = indxs[0] - 1 if len(indxs) else 0
                diag, empty = treat_r == treat_c, rob != rob
                league_table_styles.append({'if': {'filter_query': f'{{Treatment}} = {{{treat_r}}}',
                                                'column_id': treat_c},
                                                'backgroundColor': cmap[clr_indx] if not empty else CLR_BCKGRND2,
                                                'color': 'white' if not empty else CX2 if diag else 'black'})
    league_table_styles.append({'if': {'column_id': 'Treatment'}, 'backgroundColor': CX1})


    # Prepare for output
    tips = robs

    leaguetable = leaguetable.reset_index().rename(columns={'index': 'Treatment'})
    leaguetable_cols = [{"name": c, "id": c} for c in leaguetable.columns]
    leaguetable = leaguetable.to_dict('records')

    tooltip_values = [{col['id']: {'value': f"**Average ROB:** {tip[col['id']]}",
                                   'type': 'markdown'} if col['id'] != 'Treatment' else None
                           for col in leaguetable_cols} for rn, (_, tip) in enumerate(tips.iterrows())]
    if toggle_cinema:
        tooltip_values = [{col['id']: {'value': f"**Reason for Downgrading:**{tip[col['id']]}" if not comprs_downgrade.empty and not store_node else f"**Reason for Downgrading:**",
                                       'type': 'markdown'} if col['id'] != 'Treatment' else None
                       for col in leaguetable_cols} for rn, (_, tip) in enumerate(comprs_downgrade.iterrows())]
    



    data_cols = [{"name": c, "id": c} for c in net_data.columns]
    data_output = net_data[net_data.year <= slider_value].to_dict('records')
    league_table = build_league_table(leaguetable, leaguetable_cols, league_table_styles, tooltip_values)
    league_table_modal = build_league_table(leaguetable, leaguetable_cols, league_table_styles, tooltip_values, modal=True)
    _output = [data_output, data_cols] * 2 + [league_table, league_table_modal] + [legend] * 2 + [toggle_cinema, toggle_cinema_modal]

    data_and_league_table_DATA['FULL_DATA'] = net_data.to_json( orient='split')
    data_and_league_table_DATA['OUTPUT'] = _output
    data_raw_output = raw_data.to_dict('records')
    data_raw_cols = [{"name": c, "id": c} for c in raw_data.columns]
    lis = _output + _out_slider + [data_and_league_table_DATA] +[data_raw_output, data_raw_cols]
    return  _output + _out_slider + [data_and_league_table_DATA] +[data_raw_output, data_raw_cols]





def build_league_table(data, columns, style_data_conditional, tooltip_values, modal=False):

    return dash_table.DataTable(style_cell={'backgroundColor': 'rgba(0,0,0,0.1)',
                                            'color': 'black',
                                            'border': '1px solid #5d6d95',
                                            'font-family': 'sans-serif',
                                            'fontSize': 11,
                                            'minWidth': '55px',
                                            'textAlign': 'center',
                                            'whiteSpace': 'pre-line',  # 'inherit', nowrap
                                            'textOverflow': 'string'},  # 'ellipsis'
                                fixed_rows={'headers': True, 'data': 0},
                                data=data,
                                columns=columns,
                                # export_format="csv", #xlsx
                                # state='active',
                                tooltip_data= tooltip_values,
                                tooltip_delay=200,
                                tooltip_duration=None,
                                style_data_conditional=style_data_conditional,
                                # fixed_rows={'headers': True, 'data': 0},    # DOES NOT WORK / LEADS TO BUG
                                # fixed_columns={'headers': True, 'data': 1}, # DOES NOT WORK / LEADS TO BUG
                                style_header={'backgroundColor': '#738789',
                                              'border': '1px solid #5d6d95'},
                                style_header_conditional=[{'if': {'column_id': 'Treatment',
                                                                  'header_index': 0},
                                                           'fontWeight': 'bold'}],
                                style_table={'overflow': 'auto', 'width': '100%',
                                            #  'max-height': 'calc(50vh)',
                                            #  'max-width': 'calc(52vw)'
                                             } if not modal else {
                                    'overflowX': 'scroll',
                                    'overflowY': 'scroll',
                                    'height': '99%',
                                    'minWidth': '100%',
                                    'max-height': 'calc(85vh)',
                                    'width': '99%',
                                    'margin-top': '10px',
                                    'padding': '5px 5px 5px 5px'
                                },
                                css=[{"selector": '.dash-cell div.dash-cell-value',  # "table",
                                      "rule": "width: 100%; "},
                                     {'selector': 'tr:hover',
                                      'rule': 'background-color: rgba(0, 0, 0, 0);'},
                                     {'selector': 'td:hover',
                                      'rule': 'background-color: rgba(0, 116, 217, 0.3) !important;'}])






def __update_output_bothout( store_node,store_edge,toggle_cinema,
                  league_table_data, cinema_net_data, forest_data, reset_btn, outcome_idx, net_storage,filename_cinema2):
    
    if len(outcome_idx)==0:
    # If outcome_idx is None, set default values
        outcome_idx1 = 0
        outcome_idx2 = 1
    elif len(outcome_idx) > 0 and outcome_idx[0] is not None and len(outcome_idx[0]) == 2:
        # If outcome_idx exists, is non-empty, and contains two values in its first element
        outcome_idx1 = outcome_idx[0][0]
        outcome_idx2 = outcome_idx[0][1]
    else:
        # In all other cases, return an empty list
        return [], [], []


    
    reset_btn_triggered = False
    triggered = [tr['prop_id'] for tr in dash.callback_context.triggered]
    if 'reset_project.n_clicks' in triggered: reset_btn_triggered = True

    net_data = pd.read_json(net_storage[0], orient='split').round(3)



    triggered = [tr['prop_id'] for tr in dash.callback_context.triggered]
    if 'rob_vs_cinema.value' in triggered: toggle_cinema_modal = toggle_cinema
    elif 'rob_vs_cinema_modal.value' in triggered: toggle_cinema = toggle_cinema_modal


    leaguetable = pd.read_json(league_table_data[-1], orient='split')
    confidence_map = {k : n for n, k in enumerate(['low', 'medium', 'high'])}
    treatments = np.unique(net_data[['treat1', 'treat2']].dropna().values.flatten())


    net_data['rob'] = net_data['rob'].replace('__none__', '')
    net_data['rob'] = net_data['rob'].replace('.', np.nan)
    net_data['rob'] = net_data['rob'].replace('', np.nan)
    #net_data['rob'] = net_data['rob'].astype(int)

    robs = (net_data.groupby(['treat1', 'treat2']).rob.mean().reset_index()
            .pivot_table(index='treat2', columns='treat1', values='rob')
            .reindex(index=treatments, columns=treatments, fill_value=np.nan))


    robs = robs.fillna(robs.T) if not toggle_cinema else robs
    robs_slct = robs #robs + robs.T - np.diag(np.diag(robs))  if not toggle_cinema else robs ## full rob table

    comprs_downgrade  = pd.DataFrame()
    comprs_conf_lt = comprs_conf_ut = None


    if toggle_cinema:

        cinema_net_data1 = pd.read_json(cinema_net_data[0], orient='split')
        cinema_net_data2 = pd.read_json(cinema_net_data[1], orient='split')
        confidence_map = {k : n for n, k in enumerate(['very low', 'low', 'moderate', 'high'])}
        comparisons1 = cinema_net_data1.Comparison.str.split(':', expand=True)
        confidence1 = cinema_net_data1['Confidence rating'].str.lower().map(confidence_map)
        if filename_cinema2 is not None or (filename_cinema2 is None and "Default_data" in cinema_net_data2.columns):
            confidence2 = cinema_net_data2['Confidence rating'].str.lower().map(confidence_map)
        else:
            confidence2 = pd.Series(np.array([np.nan]*len(confidence1)), copy=False)
        comparisons2 = cinema_net_data2.Comparison.str.split(':', expand=True) if filename_cinema2 is not None or (filename_cinema2 is None and "Default_data" not in cinema_net_data2.columns) else comparisons1
        comprs_conf_ut = comparisons2.copy()  # Upper triangle
        comparisons1.columns = [1, 0]  # To get lower triangle
        comprs_conf_lt = comparisons1  # Lower triangle
        comprs_downgrade_lt = comprs_conf_lt
        comprs_downgrade_ut = comprs_conf_ut
        if "Reason(s) for downgrading" in cinema_net_data1.columns:
            downgrading1 = cinema_net_data1["Reason(s) for downgrading"]
            comprs_downgrade_lt['Downgrading'] = downgrading1
            if (filename_cinema2 is not None) or (filename_cinema2 is None and "Default_data" in cinema_net_data2.columns) and ("Reason(s) for downgrading" in cinema_net_data2.columns):
                downgrading2 = cinema_net_data2["Reason(s) for downgrading"]
            else:
                downgrading2 = pd.Series(np.array([np.nan]*len(downgrading1)), copy=False)
            comprs_downgrade_ut['Downgrading'] = downgrading2
            comprs_downgrade = pd.concat([comprs_downgrade_ut, comprs_downgrade_lt])
            comprs_downgrade = comprs_downgrade.pivot(index=0, columns=1, values='Downgrading')
        comprs_conf_lt['Confidence'] = confidence1
        comprs_conf_ut['Confidence'] = confidence2
        comprs_conf = pd.concat([comprs_conf_ut, comprs_conf_lt])
        comprs_conf = comprs_conf.pivot_table(index=0, columns=1, values='Confidence')


        robs = comprs_conf
        
       
    # Filter according to cytoscape selection

    if store_node and any('id' in nd for nd in store_node):
        slctd_trmnts = [nd['id'] for nd in store_node]
        if len(slctd_trmnts) > 0:
            forest_data1 = pd.read_json(forest_data[outcome_idx1], orient='split')
            net_data = pd.read_json(net_storage[0], orient='split')
            forest_data_out2 = pd.read_json(forest_data[outcome_idx2], orient='split')
            dataselectors = []
            dataselectors += [forest_data1.columns[1], net_data["outcome1_direction"].iloc[1]]
            dataselectors += [forest_data_out2.columns[1], net_data["outcome2_direction"].iloc[1]]

            leaguetable = leaguetable.loc[slctd_trmnts, slctd_trmnts]
            robs_slct = robs.loc[slctd_trmnts, slctd_trmnts]
            leaguetable_bool = pd.DataFrame(np.triu(np.ones(leaguetable.shape)).astype(bool),
                                            columns=slctd_trmnts,
                                            index=slctd_trmnts) #define upper and lower triangle

            ### pick correct comparison from FOREST_DATA and FOREST_DATA_OUT2
            for treat_c in slctd_trmnts:
                for treat_r in slctd_trmnts:
                    if treat_c != treat_r:
                        if not leaguetable_bool.loc[treat_r][treat_c]:
                            effcsze = round(forest_data1[dataselectors[0]][(forest_data1.Treatment == treat_c) & (forest_data1.Reference == treat_r)].values[0], 2)
                            ci_lower = round(forest_data1['CI_lower'][(forest_data1.Treatment == treat_c) & (forest_data1.Reference == treat_r)].values[0], 2)
                            ci_upper = round(forest_data1['CI_upper'][(forest_data1.Treatment == treat_c) & (forest_data1.Reference == treat_r)].values[0], 2)
                            leaguetable.loc[treat_r][treat_c] = f'{effcsze}\n{ci_lower, ci_upper}'
                        else:
                            pass
                        
                        effcsze2 = round(forest_data_out2[dataselectors[2]][(forest_data_out2.Treatment == treat_r) & (forest_data_out2.Reference == treat_c)].values[0], 2)
                        ci_lower2 = round(forest_data_out2['CI_lower'][(forest_data_out2.Treatment == treat_r) & (forest_data_out2.Reference == treat_c)].values[0], 2)
                        ci_upper2 = round(forest_data_out2['CI_upper'][(forest_data_out2.Treatment == treat_r) & (forest_data_out2.Reference == treat_c)].values[0], 2)

                        if leaguetable_bool.loc[treat_r][treat_c]:
                            leaguetable.loc[treat_r][treat_c] = f'{effcsze2}\n{ci_lower2, ci_upper2}'
                            if toggle_cinema: robs_slct.loc[treat_r][treat_c] = comprs_conf_ut['Confidence'][(comprs_conf_ut[0] == treat_c) & (comprs_conf_ut[1] == treat_r) |
                                                                                (comprs_conf_ut[0] == treat_r) & (comprs_conf_ut[1] == treat_c)].values[0]
                            else:
                                robs_slct.loc[treat_r][treat_c] = robs_slct[treat_r][treat_c] if not np.isnan(robs_slct[treat_r][treat_c]) else robs_slct[treat_c][treat_r]

                        else:
                            if toggle_cinema: robs_slct.loc[treat_r][treat_c] = comprs_conf_lt['Confidence'][(comprs_conf_lt[0] == treat_c) & (comprs_conf_lt[1] == treat_r) |
                                                                                (comprs_conf_lt[0] == treat_r) & (comprs_conf_lt[1] == treat_c)].values[0]
                            else:
                                robs_slct.loc[treat_r][treat_c] = robs_slct[treat_r][treat_c] if not np.isnan(robs_slct[treat_r][treat_c]) else robs_slct[treat_c][treat_r]


            leaguetable.replace(0, np.nan) #inplace

            tril_order = pd.DataFrame(np.tril(np.ones(leaguetable.shape)),
                                      columns=leaguetable.columns,
                                      index=leaguetable.columns)
            tril_order = tril_order.loc[slctd_trmnts, slctd_trmnts]
            filter = np.tril(tril_order == 0)
            filter += filter.T  # inverting of rows and columns common in meta-analysis visualissation

            robs = robs.loc[slctd_trmnts, slctd_trmnts]
            robs_values = robs.values
            #robs_values[filter] = robs_values.T[filter]
            robs = pd.DataFrame(robs_values,
                                columns=robs.columns,
                                index=robs.columns)


            treatments = slctd_trmnts

    #####   Add style colouring and legend
    N_BINS = 3 if not toggle_cinema else 4
    bounds = np.arange(N_BINS + 1) / N_BINS
    leaguetable_colr = robs.copy(deep=True)
    np.fill_diagonal(leaguetable_colr.values, np.nan)
    leaguetable_colr = leaguetable_colr.astype(np.float64)

    cmap = [CINEMA_g, CINEMA_y, CINEMA_r] if not toggle_cinema else [CINEMA_r, CINEMA_y, CINEMA_lb, CINEMA_g]
    legend_height = '4px'
    legend = [html.Div(style={'display': 'inline-block', 'width': '100px'},
                       children=[html.Div(),
                                 html.Small('Risk of bias: ' if not toggle_cinema else 'CINeMA rating: ',
                                            style={'color': 'black'})])]
    legend += [html.Div(style={'display': 'inline-block', 'width': '60px'},
                        children=[html.Div(style={'backgroundColor': cmap[n],
                                                  'height': legend_height}), html.Small(
                            ('Very Low' if toggle_cinema else 'Low') if n == 0 else 'High' if n == N_BINS - 1 else None,
                            style={'paddingLeft': '2px', 'color': 'black'})])
               for n in range(N_BINS)]
  
    cmap = [CINEMA_g, CINEMA_y, CINEMA_r] if not toggle_cinema else [CINEMA_r, CINEMA_y, CINEMA_lb, CINEMA_g]

    df_max, df_min = max(confidence_map.values()), min(confidence_map.values())
    ranges = (df_max - df_min) * bounds + df_min
    ranges[-1] *= 1.001
    ranges = ranges + 1 if not toggle_cinema else ranges
    league_table_styles = []


    for treat_c in treatments:
        for treat_r in treatments:
            if treat_r!=treat_c:
                try:
                    rob = robs.loc[treat_r, treat_c] if not store_node else robs_slct.loc[treat_r, treat_c] # Try to access the value in `robs`
                except KeyError:  # Handle errors if the value is not found
                    rob = np.nan
                # rob = robs.loc[treat_r, treat_c] if not store_node else robs_slct.loc[treat_r, treat_c]
                indxs = np.where(rob < ranges)[0] if rob == rob else [0]
                clr_indx = indxs[0] - 1 if len(indxs) else 0
                diag, empty = treat_r == treat_c, rob != rob
                league_table_styles.append({'if': {'filter_query': f'{{Treatment}} = {{{treat_r}}}',
                                                'column_id': treat_c},
                                                'backgroundColor': cmap[clr_indx] if not empty else CLR_BCKGRND2,
                                                'color': 'white' if not empty else CX2 if diag else 'black'})
                 
    league_table_styles.append({'if': {'column_id': 'Treatment'}, 'backgroundColor': CX1})
    


    # Prepare for output
    tips = robs

    leaguetable = leaguetable.reset_index().rename(columns={'index': 'Treatment'})
    leaguetable_cols = [{"name": c, "id": c} for c in leaguetable.columns]
    leaguetable = leaguetable.to_dict('records')

    # tooltip_values = [{col['id']: {'value': f"**Average ROB:** {tip[col['id']]}",
    #                                'type': 'markdown'} if col['id'] != 'Treatment' else None
    #                        for col in leaguetable_cols} for rn, (_, tip) in enumerate(tips.iterrows())]
    
    # Initialize an empty list to store tooltips
    # Iterate through the rows of the DataFrame `tips`
    tooltip_values = []
    for rn, (_, tip) in enumerate(tips.iterrows()):
        row_tooltips = {}  # Store tooltip values for the current row

        # Iterate through the columns in `leaguetable_cols`
        for col in leaguetable_cols:    
            if col['id'] == 'Treatment':  # Special case: no tooltip for 'Treatment' column
                row_tooltips[col['id']] = None
            else:
                try:
                    rob_v = tip[col['id']]  # Try to access the value in the column
                except KeyError:  # Handle missing column gracefully
                    rob_v = None

                # Add a tooltip value for this column
                if rob_v is not None:  # If value exists
                    row_tooltips[col['id']] = {'value': f"**Average ROB:** {rob_v}", 'type': 'markdown'}
                else:  # If value is missing or causes an error
                    row_tooltips[col['id']] = {'value': "**Average ROB:** N/A", 'type': 'markdown'}

        # Append the tooltips for this row to the list
        tooltip_values.append(row_tooltips)

    if toggle_cinema:
        tooltip_values = []
        # tooltip_values = [{col['id']: {'value': f"**Reason for Downgrading:**{tip[col['id']]}" if not comprs_downgrade.empty and not store_node else f"**Reason for Downgrading:**",
        #                                'type': 'markdown'} if col['id'] != 'Treatment' else None
        #                for col in leaguetable_cols} for rn, (_, tip) in enumerate(comprs_downgrade.iterrows())]
        
        for rn, (_, tip) in enumerate(comprs_downgrade.iterrows()):
                row_tooltips = {}  # Store tooltip values for the current row

                # Iterate through the columns in `leaguetable_cols`
                for col in leaguetable_cols:
                    if col['id'] == 'Treatment':  # No tooltip for the 'Treatment' column
                        row_tooltips[col['id']] = None
                    else:
                        # Determine the tooltip value based on conditions
                        if not comprs_downgrade.empty:
                            reason = tip[col['id']] if col['id'] in tip else ""
                            tooltip_text = f"**Reason for Downgrading:** {reason}"
                        else:
                            tooltip_text = "**Reason for Downgrading:**"

                        # Assign the tooltip for this column
                        row_tooltips[col['id']] = {'value': tooltip_text, 'type': 'markdown'}

                # Append the tooltips for this row to the list
                tooltip_values.append(row_tooltips)

  

    if store_edge or store_node:
        slctd_nods = {n['id'] for n in store_node} if store_node else set()
        slctd_edgs = [e['source'] + e['target'] for e in store_edge] if store_edge else []
        net_data = net_data[net_data.treat1.isin(slctd_nods) | net_data.treat2.isin(slctd_nods)
                    | (net_data.treat1 + net_data.treat2).isin(slctd_edgs) | (net_data.treat2 + net_data.treat1).isin(slctd_edgs)]


    
    league_table = build_league_table(leaguetable, leaguetable_cols, league_table_styles, tooltip_values)
    # _output =  [league_table] + [legend] + [toggle_cinema]


    return  league_table, legend, toggle_cinema


