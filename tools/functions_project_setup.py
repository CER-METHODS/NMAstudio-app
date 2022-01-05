import dash_html_components as html
import dash_bootstrap_components as dbc
from assets.COLORS import *
import dash_core_components as dcc

options_effect_size_cont = [{'label':'MD',  'value':'MD'}, {'label':'SMD',     'value':'SMD'}]
options_effect_size_bin = [{'label':'OR',  'value':'OR'}, {'label':'RR',     'value':'RR'}]

def __update_options(search_value_format, search_value_outcome1, search_value_outcome2):

    if search_value_format is None: return None
    if search_value_outcome1 is None: return None

    name_outcomes = ['1st outcome*', '2nd outcome'] if search_value_outcome2 is not None else ['1st outcome']
    search_values = [search_value_outcome1, search_value_outcome2] if search_value_outcome2 is not None else [search_value_outcome1]
    selectors_ef = html.Div([html.Div(
        [dbc.Row([html.P("Select effect size", style={'color': 'white', 'vertical-align': 'middle'})])] +
         [dbc.Row([dbc.Col(dbc.Row(
                  [html.P(f"{name}", className="selectbox", style={'display': 'inline-block', "text-align": 'right',
                                                                   'margin-left': '0px', 'font-size': '12px'}),
                  dcc.Dropdown(id={'type': 'dataselectors', 'index': f'dropdown-{name_outcomes}'},
                               options=options_effect_size_cont if val=='continuous' else options_effect_size_bin,
                               searchable=True, placeholder="...",
                               clearable=False, style={'width': '60px', "height":'20px',
                                                       'vertical-align': 'middle',
                                                       "font-size": "1em",
                                                       "font-family": "sans-serif",
                                                       'margin-bottom': '10px',
                                                       'display': 'inline-block',
                                                       'color': CLR_BCKGRND_old, 'font-size': '10px',
                                                       'background-color': CLR_BCKGRND_old} )]
          ),  style={'margin-left': '55px', 'margin-right': '5px'}) for name, val in zip(name_outcomes, search_values)]
        )],
     )])
    return selectors_ef