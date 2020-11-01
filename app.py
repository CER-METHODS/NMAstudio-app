import os, io
import pandas as pd, numpy as np
import dash, dash_core_components as dcc, dash_html_components as html
import dash_table


import dash_cytoscape as cyto

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import plotly.express as px

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

app = dash.Dash(__name__, meta_tags=[{"name": "viewport",
                                      "content": "width=device-width, initial-scale=1"}])

server = app.server
stylesheet = [{'selector': 'node',
               'style': {'content': 'data(name)',
                         'font-family': 'helvetica',
                         'font-size': 18,
                         'text-outline-width': 1,
                         # 'text-outline-color': '#fff',
                         'opacity': 1,
                         'label': "data(label)",
                         'background-color': "#07ABA0",
                         'color': "#fff"}},
              {'selector': 'edge',
               'style': {'line-color': "#C5D3E2",
                         'arrow-scale': 2,
                         'width': 'data(weight)',
                         'curve-style': 'bezier'}}
             ]

network_layouts = [{'label': 'circle',       'value': 'circle'},
                   {'label': 'random',       'value': 'random'},
                   {'label': 'grid',         'value': 'grid'},
                   {'label': 'concentric',   'value': 'concentric'},
                   {'label': 'breadthfirst', 'value': 'breadthfirst'},
                   {'label': 'cose',         'value': 'cose'}]

DF = pd.read_csv('db/Senn2013.csv', index_col=0).rename(columns={"treat1.long": 'from',
                                                                 "treat2.long": 'to'})
def get_network():
    edges = DF.groupby(['from', 'to']).TE.count().reset_index()
    cy_edges = [{'data': {'source': source, 'target': target, 'weight': weight * 2, 'weight_lab': weight}}
                for source, target, weight in edges.values]
    cy_nodes = [{"data": {"id": target, "label": target}}
                for target in np.unique(edges[['from', 'to']].values.flatten())]

    return cy_edges + cy_nodes



app.layout = html.Div(
    [html.Div(  # header
             [html.Div([html.H4("Pis è un babbeo", className="app__header__title"),
                        html.P("Anche se questo si è sempore saputo e non è dunque una gran novità...",
                               className="app__header__title--grey")], className="app__header__desc"),
             html.Div([html.Img(src=app.get_asset_url("logo_universite_paris.jpg"),
                                className="app__menu__img")],
                      className="app__header__logo")],
             className="app__header"),
    html.Div([html.Div(   # NMA Graph
                 [html.Div([html.H6("NMA Graph", className="graph__title",style={'display': 'inline-block'}),
                            html.Div([dcc.Dropdown(id='dropdown-layout', options=network_layouts, clearable=False,
                                                   value='circle', style={'width':'170px',
                                                                          'color': '#1b242b',
                                                                          'background-color': '#40515e'})],
                            className="row")]),
                  cyto.Cytoscape(id='cytoscape',
                                 elements=get_network(),
                                 style={'height': '70vh', 'width': '100%'},
                                 stylesheet=stylesheet)],
                  className="one-half column"),
              html.Div(
                      [html.Div(  # Information
                           [html.Div([html.H6("Information", className="box__title")]),
                            html.Div([html.P(id='cytoscape-mouseoverEdgeData-output', className="info_box"),
                                      html.Br()],
                                      className="content_information"),
                            html.Div([],className="auto__container")],
                          className="info__container"),
                          # Forest Plot
                          html.Div([dcc.Tabs([
                              dcc.Tab(label='Forest plot',
                                      children=[html.Div([html.P(id='tapNodeData-info', className="box__title"),
                                                          html.Br()]),
                                                dcc.Loading(
                                                    dcc.Graph(id='tapNodeData-fig',
                                                              config={'modeBarButtonsToRemove':['toggleSpikelines', "pan2d",
                                                                                                "select2d", "lasso2d", "autoScale2d",
                                                                                                "hoverCompareCartesian"],
                                                                      'toImageButtonOptions': {'format': 'png', # one of png, svg,
                                                                                               'filename': 'custom_image',
                                                                                               'scale': 10 # Multiply title/legend/axis/canvas sizes by this factor
                                                                                              },
                                                                      'displaylogo':False}))]
                                      ),
                              dcc.Tab(label='Data', children=[dcc.Upload(html.Button('Upload your file!',
                                                                                     style=dict(color='white')),
                                                                         id='datatable-upload'),
                                                              dash_table.DataTable(id='datatable-upload-container',
                                                                                   fixed_rows={'headers': True,
                                                                                               'data': 0},
                                                                                   style_cell_conditional=[
                                                                                       {'if': {'column_id': c},
                                                                                               'textAlign': 'left'}
                                                                                       for c in ['Date', 'Region']],
                                                                                   style_data_conditional=[
                                                                                       {'if': {'row_index': 'odd'},
                                                                                               'backgroundColor': 'rgb(248, 248, 248)'}],
                                                                                   style_header={'backgroundColor': 'rgb(230, 230, 230)',
                                                                                                 'fontWeight': 'bold'},
                                                                                   css=[{"selector": "table",
                                                                                             "rule": "width: 100%;"}]
                                                                                   )])
                          ],colors={"border": "#1b242b",
                                    "primary": "#1b242b",
                                    "background": "#1b242b"}, style=dict(color='#40515e', fontWeight= 'bold')),
                          ],
                                   className="graph__container second"),

                      ],
                      className="one-half column"),


    ],
              className="app__content")],
    className="app__container")




@app.callback(Output('cytoscape', 'layout'),
             [Input('dropdown-layout', 'value')])
def update_cytoscape_layout(layout):
    return {'name': layout,
            'animate': True}



@app.callback(Output('tapNodeData-info', 'children'),
              [Input('cytoscape', 'tapNodeData')])
def TapNodeData_info(data):
    if data:
        return data['label']
    else:
        return 'Click on a node to display associated forest plot'

@app.callback(Output('tapNodeData-fig', 'figure'),
              [Input('cytoscape', 'tapNodeData')])
def TapNodeData_fig(data):
    if data:
        treatment = data['label']
        df = pd.read_csv(f'db/forest_data/{treatment}.csv').reset_index(drop=False)
        df['CI_width'] = df.CI_upper - df.CI_lower
        df = df.sort_values(by='RR')
    else:
        df = pd.DataFrame([[0]*7]*12, columns=['index', 'Treatment', 'RR', 'CI_lower', 'CI_upper', 'WEIGHTS', 'CI_width'])

    fig = px.scatter(df, x="RR", y="Treatment",
                     error_x_minus='CI_lower', error_x='CI_width',
                     size='WEIGHTS',
                     log_x=True)
    fig.update_layout(paper_bgcolor='#40515e',
                      plot_bgcolor='#40515e')
    fig.add_shape(type='line',
                  yref='paper', y0=0, y1=1,
                  xref='x', x0=1, x1=1,
                  line=dict(color="white", width=1), layer='below')
    fig.update_traces(marker=dict(symbol='square', opacity=1, line=dict(color='MediumPurple')))
    fig.update_xaxes(ticks="outside", tickwidth=2, tickcolor='white', ticklen=5,
                     tickvals=[0.1, 0.5, 1, 5, 10], ticktext=[0.1, 0.5, 1, 5, 10],
                     autorange=True, showline=True, zeroline=True, range=[0.1, 1])
    fig.update_layout(clickmode='event+select',
                      font_color="white",
                      margin=dict(l=0, r=10, t=12, b=80),
                      xaxis=dict(showgrid=False, tick0=0),
                      yaxis=dict(showgrid=False, title=''),
                      title_text='Treatment', title_x=0.02, title_y=.98, title_font_size=14,
                      annotations=[dict(x=-1, ax=0, y=-0.15, ay=-0.1, xref='x', axref='x', yref='paper',
                                        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3, arrowcolor='green'),
                                   dict(x=1, ax=0, y=-0.15, ay=-0.1, xref='x', axref='x', yref='paper',
                                        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3, arrowcolor='red'),
                                   dict(x=.1, y=-0.22, xref='paper', yref='paper', text='Favours treatment',
                                        showarrow=False),
                                   dict(x=.78, y=-0.22, xref='paper', yref='paper', text='Favours PVI',
                                        showarrow=False)] if data else [])
    if not data:
        fig.update_yaxes(tickvals=[], ticktext=[], visible=False)
        fig.update_layout(margin=dict(l=0, r=10, t=12, b=80))

    return fig




# @app.callback(Output('cytoscape-tapEdgeData-output', 'children'),
#               [Input('cytoscape', 'tapEdgeData')])
# def TapEdgeData(data):
#     if data:
#         return "Clicked on edge between " + data['source'].upper() + " and " + data['target'].upper()


# @app.callback(Output('cytoscape-mouseoverNodeData-output', 'children'),
#               [Input('cytoscape', 'mouseoverNodeData')])
# def mouseoverNodeData(data):
#     if data:
#         return "Hovered over node: " + data['label']



@app.callback(Output('cytoscape-mouseoverEdgeData-output', 'children'),
              [Input('cytoscape', 'mouseoverEdgeData')])
def mouseoverEdgeData(data):
    if data:
        n_studies = data['weight_lab']
        studies_str = f"{n_studies}" + (' studies' if n_studies>1 else ' study')
        return f"{data['source'].upper()} vs {data['target'].upper()}: {studies_str}"
    else:
        return "Try hovering over an edge!"

# @app.callback(Output('datatable-upload-container', 'children'),
#               [Input('upload', 'contents')])
# def update_figure(content):
#     if not content:
#         return []
#     dff = pd.read_csv(io.StringIO(content))
#     return dff.to_dict('records')
import base64
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        return pd.read_excel(io.BytesIO(decoded))


@app.callback([Output('datatable-upload-container', 'data'),
               Output('datatable-upload-container', 'columns')],
              [Input('datatable-upload', 'contents')],
              [State('datatable-upload', 'filename')])
def update_output(contents, filename):
    if contents is None:
        df = DF
    else:
        df = parse_contents(contents, filename)
    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]



if __name__ == "__main__":
    app.run_server(debug=False)
