import numpy as np
import pandas as pd
import datetime
from assets.dropdowns_values import *
from tools.utils import set_slider_marks
default_data = pd.read_csv('db/psoriasis_wide_complete.csv')

YEARS_DEFAULT = np.array(
    [
        1963,
        1990,
        1997,
        2001,
        2003,
        2004,
        2005,
        2006,
        2007,
        2008,
        2010,
        2011,
        2012,
        2013,
        2014,
        2015,
        2016,
        2017,
        2018,
        2019,
        2020,
        2021,
    ]
)


def tab_data(years=YEARS_DEFAULT):
    y_max, y_min = years.max(), years.min()
    return html.Div(
        [ 
            html.Div([
                dcc.Slider(
                    min=y_min,
                    max=y_max,
                    step=50,
                    marks=set_slider_marks(y_min, y_max, years),
                    value=datetime.date.today().year,  # ymax
                    updatemode="drag",
                    id="slider-year",
                    tooltip=dict(placement="top"),
                ),
                html.Div([ html.P("Click the slider to see the evolution of the evidence over time. The data table will be filtered accordingly in real-time.",
                              id='slider-instruction',),
                html.A(
                 html.Img(
                    src="/assets/icons/query.png",
                    style={
                        "width": "16px",
                        "margin-top": "0px",
                        "border-radius": "0px",},
                )),
                ],id="query-icon",),
                ],
                style={
                    "display": "inline-block",
                    "width": "50%",
                    "float": "right",
                    "color": CLR_BCKGRND2,
                    "padding-top": "25px",
                    "margin-right": "10px",
                    "margin-left": "15px",
                }, id='slider-container'
        ), 

            html.Br(),html.Br(),html.Br(),
            dash_table.DataTable(
                id="datatable-upload-container",
                editable=False,
                # data = default_data.to_dict('records'),
                # columns=[{"name": c, "id": c} for c in default_data.columns],
                # export_format="csv",
                fixed_rows={"headers": True, "data": 0},
                style_cell={
                    "backgroundColor": "white",
                    "color": "black",
                    "minWidth": "45px",
                    "maxWidth": "60px",
                    "textAlign": "center",
                    "border": "1px solid #5d6d95",
                    "overflow": "hidden",
                    "whiteSpace": "no-wrap",
                    "textOverflow": "ellipsis",
                    "font-family": "sans-serif",
                    "fontSize": 11,
                },
                style_data_conditional=[
                    {"if": {"row_index": "odd"}, "backgroundColor": "rgba(0,0,0,0.1)"},
                    {
                        "if": {"state": "active"},
                        "backgroundColor": "rgba(0, 116, 217, 0.3)",
                        "border": "1px solid rgb(0, 116, 217)",
                    },
                ],
                style_header={
                    # "backgroundColor": "#738789",
                    'backgroundColor': '#f5c198',
                    "fontWeight": "bold",
                    "border": "1px solid #5d6d95",
                },
                style_table={
                    "overflowX": "auto",
                    "overflowY": "auto",
                    "height": "99%",
                    "max-height": "420px",
                    "minWidth": "100%",
                    "width": "99%",
                    "max-width": "calc(52vw)",
                    "padding": "5px 5px 5px 5px",
                },
                css=[
                    {
                        "selector": "tr:hover",
                        "rule": "background-color: rgba(0, 0, 0, 0);",
                    },
                    {
                        "selector": "td:hover",
                        "rule": "background-color: rgba(0, 116, 217, 0.3) !important;",
                    },
                ],
            ),
        ],
        style={"overflowX": "scroll", "overflowY": "scroll"},
    )


def raw_data():

    return html.Div(
        [   html.Br(),html.Br(),html.Br(),
            dash_table.DataTable(
                id="datatable-raw-container",
                editable=False,
                # data = default_data.to_dict('records'),
                # columns=[{"name": c, "id": c} for c in default_data.columns],
                # export_format="csv",
                fixed_rows={"headers": True, "data": 0},
                style_cell={
                    "backgroundColor": "white",
                    "color": "black",
                    "minWidth": "45px",
                    "maxWidth": "60px",
                    "textAlign": "center",
                    "border": "1px solid #5d6d95",
                    "overflow": "hidden",
                    "whiteSpace": "no-wrap",
                    "textOverflow": "ellipsis",
                    "font-family": "sans-serif",
                    "fontSize": 11,
                },
                style_data_conditional=[
                    {"if": {"row_index": "odd"}, "backgroundColor": "rgba(0,0,0,0.1)"},
                    {
                        "if": {"state": "active"},
                        "backgroundColor": "rgba(0, 116, 217, 0.3)",
                        "border": "1px solid rgb(0, 116, 217)",
                    },
                ],
                style_header={
                    # "backgroundColor": "#738789",
                    'backgroundColor': '#f5c198',
                    "fontWeight": "bold",
                    "border": "1px solid #5d6d95",
                },
                style_table={
                    "overflowX": "auto",
                    "overflowY": "auto",
                    "height": "99%",
                    "max-height": "420px",
                    "minWidth": "100%",
                    "width": "99%",
                    "max-width": "calc(52vw)",
                    "padding": "5px 5px 5px 5px",
                },
                css=[
                    {
                        "selector": "tr:hover",
                        "rule": "background-color: rgba(0, 0, 0, 0);",
                    },
                    {
                        "selector": "td:hover",
                        "rule": "background-color: rgba(0, 116, 217, 0.3) !important;",
                    },
                ],
            ),
        ],
        style={"overflowX": "scroll", "overflowY": "scroll"},
    )
