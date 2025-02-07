import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Input, Output, State, html, dcc
from assets.Tabs.saveload_modal_button import saveload_modal

NMASTUDIO_LOGO = "/assets/logos/NMAstudio_bold.png"
CRESS_LOGO = "/assets/logos/CRESS_logo.png"
UP_LOGO = "/assets/logos/logo_universite_paris.jpg"


def Navbar():
    realhome_button = dbc.NavItem(dbc.NavLink('HOME', href="/home", external_link=True,
                                          style = {'color':'#white','font-family': "sans-serif ",
                                                   'font-size': '15px'}))
    home_button = dbc.NavItem(dbc.NavLink('RESULTS', href="/results", external_link=True,
                                          style = {'color':'#white','font-family': "sans-serif ",
                                                   'font-size': '15px'}))
    skt_button = dbc.NavItem(dbc.NavLink('Knowledge Translation (under construction)', href="/skt",external_link=True,
                                         style = {'color':'lightsteelblue','font-family': "sans-serif ",
                                                  'font-size': '15px'}, id= 'skt_button'))
    setup_button = dbc.NavItem(dbc.NavLink('Setup Analysis (under construction)', href="/setup",external_link=True,
                                         style = {'color':'lightsteelblue','font-family': "sans-serif ",
                                                  'font-size': '15px'}, id= ''))
    # skt_button = dbc.NavItem(dbc.NavLink('SKT TOOL', n_click=0,
    #                                      style = {'color':'#white','font-family': "sans-serif ",
    #                                               'font-size': '13px', 'pointer-events': 'stroke',
    #                                               'padding': 'unset',
    #                                               'margin-top':'-7px', 'border': 'none'}, id= 'skt_button'))

    # doc_button = dbc.NavItem(dbc.NavLink('DOCUMENTATION', href="/doc", external_link=True,
    #                                      style = {'color':'#white','font-family': "sans-serif ",
    #                                               'font-size': '13px' }))
    # news_button = dbc.NavItem(dbc.NavLink('NEWS', href="/news", external_link=True,
    #                                      style = {'color':'#white','font-family': "sans-serif ",
    #                                               'font-size': '13px' }))


    # saveload_button = saveload_modal

    navbar = dbc.Navbar([
            html.Div(dbc.Col(html.Img(src=NMASTUDIO_LOGO, height="53px",
                                      style={'filter': 'invert()',
                                             # 'filter': 'invert(42 %) sepia(26 %) saturate(2474 %) hue-rotate(218deg) brightness(97 %) contrast(89 %)',
                                              #'filter': 'invert(44%) sepia(57%) saturate(3117%) hue-rotate(147deg) brightness(99%) contrast(94%)',
                                              'padding-left': '2%','padding-right': '2%',
                                              'padding-bottom':'0.4%','padding-top':'0.4%',
                                              'margin-left':'50px'}),
                             className="child", sm=3, md=2),
                     style={
                            #"border": "0.01px white solid",
                            'padding-bottom':'0.6%','padding-left':'0.6%',
                            'padding-right':'0.6%', 'padding-top':'0.6%',
                           # 'background-color':'#304569'
                            }),

            html.Div([
                dbc.Col(children=[dbc.Nav([realhome_button, home_button, setup_button, skt_button],
                                          navbar=True, style={'text-align':'center',
                                                              'padding-right':'5%','padding-top':'2.5%',
                                                              'margin-left':'50px',
                                                              'justify-content': 'end'}),
                          ]),

                #Toggle theme
                # dbc.Col([html.P(
                #     "Light",
                #     id='light_theme',
                #     style={'display': 'inline-block',
                #            'margin': 'auto', 'color':'white',
                #            'font-size': '10px',
                #            'padding-left': '0px'}),
                #     daq.ToggleSwitch(
                #         id='toggleTheme', value=True, color="#00418e",
                #         size=40, vertical=False,
                #         label={'label': "",
                #                'style': dict(color='white', font='0.5em')},
                #         labelPosition="top",
                #         style={'display': 'inline-block',
                #                'margin': 'auto', 'font-size': '10px',
                #                'padding-left': '2px',
                #                'padding-right': '2px'}),
                #     html.P('Dark',
                #            id='dark_theme',
                #            style={'display': 'inline-block',
                #                   'margin': 'auto', 'color':'white',
                #                   'font-size': '10px',
                #                   'padding-right': '10px'})
                #
                # ], style={'display': 'inline-block',
                #           'margin-top': '10px',  'margin-right': '25px'}
                # ),
                # dbc.Col(html.Img(src=UP_LOGO, height="57px"), style={'padding-right':'1%','padding-top':'0.3%','padding-bottom':'0.3%'},
                #     width="auto")
                    ], className="child child-right" ),
        ],
        color="#5c7780",
        dark=True,
    )

    return navbar
