import plotly.express as px, plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc, dash_html_components as html
import numpy as np

def display_modal_barplot(cell, value, rowdata):
    # print(cell)
    if cell is None or len(cell) == 0: 
        fig = go.Figure(data=[], layout={})
        header = html.P("") 
        return fig, header
    
    rowdata = pd.DataFrame(rowdata)
    if ('colId' in cell and cell['colId'] == "RR"):
        first_part = cell['value'].split('\n')[0]
        rr = float(first_part)
        row_idx = cell['rowIndex']
        treatment = rowdata.loc[row_idx, 'Treatment']
        compare = rowdata.loc[row_idx, 'Reference']
        header = html.P(f"{treatment} VS {compare}")
    else: 
        fig = go.Figure(data=[], layout={})
        header = html.P("") 
        return fig, header

    annotations = []

    if value:
        value = int(value)
        ab_treat = int(rr*value)
        x_data = [ab_treat, value]
        y_data = [treatment, compare]
        y_value_dict = {category: index for index, category in enumerate(y_data)}
        fig = go.Figure(go.Bar(
            x=x_data,
            y=y_data,
            marker_color=['rgb(241,197,13)', ' rgb(128, 191, 69)'],
            orientation='h'))
        for yd, xd in zip(y_data, x_data):
            yd_position = y_value_dict[yd]
            annotations.append(dict(xref='x', yref='y',
                                        x=xd/2, y=yd_position+0.5,
                                        text=str(xd) + ' per 1000',
                                        font=dict(family='Arial', size=14,
                                                color='black'),
                                        showarrow=False))
        
    else:
        ab_treat = int(rr*20)
        x_data = [ab_treat, 20]
        y_data = [treatment, compare]
        y_value_dict = {category: index for index, category in enumerate(y_data)}
        fig = go.Figure(go.Bar(
            x=x_data,
            y=y_data,
            marker_color=['rgb(241,197,13)', ' rgb(128, 191, 69)'],
            orientation='h'))
        for yd, xd in zip(y_data, x_data):
            yd_position = y_value_dict[yd]
            annotations.append(dict(xref='x', yref='y',
                                        x=xd/2, y=yd_position+0.5,
                                        text=str(xd) + ' per 1000',
                                        font=dict(family='Arial', size=14,
                                                color='black'),
                                        showarrow=False))
    
    fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',  # transparent bg
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            width = 350,
            height = 150,
            autosize=True,
            bargap=0.3,
            bargroupgap=0.2,
            annotations=annotations,
            xaxis=dict(showgrid=False,
                        showline=False,
                        showticklabels=False,
                        zeroline=False,)
        )
    
   
    return fig, header


def display_modal_text(cell,value,rowdata):
    if cell is None or len(cell) == 0: 
        # risk_range = html.P("") 
        info_col = html.Span('')
        return info_col
    
    rowdata = pd.DataFrame(rowdata)
    if ('colId' in cell and cell['colId'] == "RR"):
        
        if value:
            value = int(value)
        else:
            value = 20
        
        first_part = cell['value'].split('\n')[0]
        rr = float(first_part)
        row_idx = cell['rowIndex']
        treatment = rowdata.loc[row_idx, 'Treatment']
        compare = rowdata.loc[row_idx, 'Reference']
        
        ab_treat = int(rr*value)
        ab_diff = ab_treat-value
        span_diff = f"{ab_diff} more per 1000" if ab_diff > 0 else f"{abs(ab_diff)} less per 1000"
        
        rr_low = rowdata.loc[row_idx, 'CI_lower']
        ab_diff_low = int(rr_low*value)-value
        span_diff_low = f"{ab_diff_low} more per 1000" if ab_diff_low > 0 else f"{abs(ab_diff_low)} less per 1000"

        rr_up = rowdata.loc[row_idx, 'CI_upper']
        ab_diff_up = int(rr_up*value)-value
        span_diff_up = f"{ab_diff_up} more per 1000" if ab_diff_up > 0 else f"{abs(ab_diff_up)} less per 1000"
    
    else:
        return ''
    
    span1 = html.Span("Outcome: PASI90", className="skt_span_info2", id="treat_comp")
    span2 = html.Span(f"Treatment: {treatment}", className="skt_span_info2", id="num_RCT")
    span3 = html.Span(f"Comparator: {compare}", className="skt_span_info2", id="num_RCT")
    span4 = html.Span(
                        f"Absolute difference: {span_diff}", 
                        className="skt_span_info2", 
                        id="num_sample"
                    )
    span5 = html.Span(
                       f"CI: {span_diff_low} to {span_diff_up}",
                        className="skt_span_info2",
                        id="mean_modif"
                        )
    children = [span1, span2, span3, span4, span5]

    return children

