import os, shutil, pickle, base64, io
import string
import random
from pandas.api.types import is_numeric_dtype
from tools.PATHS import __TEMP_LOGS_AND_GLOBALS, __SESSIONS_FOLDER, YESTERDAY
from assets.effect_sizes import *
# ---------R2Py Resources --------------------------------------------------------------------------------------------#
import rpy2
from rpy2.robjects import pandas2ri  # Define the R script and loads the instance in Python
#pandas2ri.activate()
import rpy2.robjects as ro
import rpy2.rinterface_lib as rlib
from rpy2.robjects.conversion import localconverter
#import plotly.express as px

import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector


# utils = rpackages.importr('base')

# # import R's utility package
# utils = rpackages.importr('utils')

# # select a mirror for R packages
# utils.chooseCRANmirror(ind=1) # select the first mirror in the list

# # R package names
# packnames = ("dplyr","tidyverse", "metafor","netmeta")

# # R vector of strings
# from rpy2.robjects.vectors import StrVector

# # Selectively install what needs to be install.
# # We are fancy, just because we can.
# names_to_install = [x for x in packnames if not rpackages.isinstalled(x)]
# if len(names_to_install) > 0:
#     utils.install_packages(StrVector(names_to_install))



r = ro.r
r['source']('R_Codes/all_R_functions.R')  # Loading the function we have defined in R.
run_NetMeta_r = ro.globalenv['run_NetMeta_new']  # Get run_NetMeta from R
league_table_r = ro.globalenv['league_rank_new']  # Get league_table from R
league_table_r_both = ro.globalenv['league_both']  # Get league_table_both from R
pairwise_forest_r = ro.globalenv['pairwise_forest_new']  # Get pairwise_forest from R
funnel_plot_r = ro.globalenv['funnel_funct_new']  # Get pairwise_forest from R
run_pairwise_data_long_r = ro.globalenv['get_pairwise_data_long_new']  # Get pairwise data from long format from R
run_pairwise_data_contrast_r = ro.globalenv['get_pairwise_data_contrast_new']  # Get pairwise data from contrast format from R


## read R console for printing errors
def  my_consoleread(promp: str) -> str:
    custom_prompt = f'R is asking this: {promp}'
    return input(custom_prompt)

def print_console_error():
    rlib.callbacks.consoleread = my_consoleread

def apply_r_func(func, df):
    df['rob'] = df['rob'].astype("string")
    df['rob'] = (df['rob'].str.lower()
                      .str.strip()
                      .replace({'low': 'l', 'medium': 'm', 'high': 'h'})
                      .replace({'l': 1, 'm': 2, 'h': 3}))
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_r = ro.conversion.py2rpy(df.reset_index(drop=True))
    func_r_res = func(dat=df_r)
    r_result = pandas2ri.rpy2py(func_r_res)

    if isinstance(r_result, ro.vectors.ListVector):
        with localconverter(ro.default_converter + pandas2ri.converter):
            leaguetable, pscores, consist, netsplit, netsplit_all  = (ro.conversion.rpy2py(rf) for rf in r_result)
        return leaguetable, pscores, consist, netsplit, netsplit_all
    else:
        df_result = r_result.reset_index(drop=True)  # Convert back to a pandas.DataFrame.
        return df_result



def apply_r_func_new(func, df, i):
    df['rob'] = df['rob'].astype("string")
    df['rob'] = (df['rob'].str.lower()
                        .str.strip()
                        .replace({'low': 'l', 'medium': 'm', 'high': 'h'})
                        .replace({'l': 1, 'm': 2, 'h': 3}))
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_r = ro.conversion.py2rpy(df.reset_index(drop=True))

    func_r_res = func(dat=df_r, i=i)
    r_result = pandas2ri.rpy2py(func_r_res)

    if isinstance(r_result, ro.vectors.ListVector):
        with localconverter(ro.default_converter + pandas2ri.converter):
            leaguetable, pscores, consist, netsplit, netsplit_all  = (ro.conversion.rpy2py(rf) for rf in r_result)
        return leaguetable, pscores, consist, netsplit, netsplit_all
    else:
        df_result = r_result.reset_index(drop=True)  # Convert back to a pandas.DataFrame.
        return df_result


def apply_r_func_new_lt(func, df, i, j):
    df['rob'] = df['rob'].astype("string")
    df['rob'] = (df['rob'].str.lower()
                        .str.strip()
                        .replace({'low': 'l', 'medium': 'm', 'high': 'h'})
                        .replace({'l': 1, 'm': 2, 'h': 3}))
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_r = ro.conversion.py2rpy(df.reset_index(drop=True))
    func_r_res = func(dat=df_r, i=i, j=j)
    r_result = pandas2ri.rpy2py(func_r_res)
    if isinstance(r_result, ro.vectors.ListVector):
        with localconverter(ro.default_converter + pandas2ri.converter):
            leaguetable = (ro.conversion.rpy2py(rf) for rf in r_result)
        return leaguetable
    else:
        df_result = r_result.reset_index(drop=True)  # Convert back to a pandas.DataFrame.
        return df_result
# def apply_r_func_two_outcomes(func, df):
#     df['rob'] = df['rob'].astype("string")
#     df['rob'] = (df['rob'].str.lower()
#                  .str.strip()
#                  .replace({'low': 'l', 'medium': 'm', 'high': 'h'})
#                  .replace({'l': 1, 'm': 2, 'h': 3}))
#     with localconverter(ro.default_converter + pandas2ri.converter):
#         df_r = ro.conversion.py2rpy(df.reset_index(drop=True))
#     func_r_res = func(dat=df_r, outcome2=True)
#     r_result = pandas2ri.rpy2py(func_r_res)

#     if isinstance(r_result, ro.vectors.ListVector):
#         with localconverter(ro.default_converter + pandas2ri.converter):
#             leaguetable, pscores, consist, netsplit, netsplit2, netsplit_all, netsplit_all2 = (ro.conversion.rpy2py(rf) for rf in r_result)
#         return leaguetable, pscores, consist, netsplit, netsplit2, netsplit_all, netsplit_all2
#     else:
#         df_result = r_result.reset_index(drop=True)  # Convert back to a pandas.DataFrame.
#         return df_result



def apply_r_func_two_outcomes(func, df, num_outcomes):
    df['rob'] = df['rob'].astype("string")
    df['rob'] = (df['rob'].str.lower()
                 .str.strip()
                 .replace({'low': 'l', 'medium': 'm', 'high': 'h'})
                 .replace({'l': 1, 'm': 2, 'h': 3}))
    with localconverter(ro.default_converter + pandas2ri.converter):
        df_r = ro.conversion.py2rpy(df.reset_index(drop=True))
    func_r_res = func(dat=df_r, num_outcome = num_outcomes)
    r_result = pandas2ri.rpy2py(func_r_res)

    if isinstance(r_result, ro.vectors.ListVector):
        with localconverter(ro.default_converter + pandas2ri.converter):
            leaguetable, pscores, consist, netsplit, netsplit2, netsplit_all, netsplit_all2 = (ro.conversion.rpy2py(rf) for rf in r_result)
        return leaguetable, pscores, consist, netsplit, netsplit2, netsplit_all, netsplit_all2
    else:
        df_result = r_result.reset_index(drop=True)  # Convert back to a pandas.DataFrame.
        return df_result




# ----------------------------------------------------------------------------------
## -------------------------------------------------------------------------------- ##

def generate_ssl_perm_and_key(cert_name, key_name):
    os.system(f"""openssl req -newkey rsa:4096 \
                                 -x509 \
                                 -sha256 \
                                 -days 3650 \
                                 -nodes \
                                 -out {cert_name} \
                                 -keyout {key_name} \
                                 -subj '/C=FR/ST=Paris/L=Paris/O=Security/OU=CRESS/CN=www.nmastudioapp.com'""")
    return cert_name, key_name

# def write_session_pickle(dct, path):
#     with open(path, 'wb') as f:
#         pickle.dump(dct, f, protocol=pickle.HIGHEST_PROTOCOL)
# def read_session_pickle(path):
#     return pickle.load(open(path, 'rb'))


def id_generator(chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(len(chars)))

## --------------------------------MISC-------------------------------------------- ##
def set_slider_marks(y_min, y_max, years):
    return {int(x): {'label': str(x),
                     'style': {'color': 'black', 'font-size':'10px',
                               'opacity':1 if x in (y_min, y_max) else 0}}
            for x in np.unique(years).astype('int')
            }



## ----------------------------  NETWORK FUNCTION --------------------------------- ##
CMAP = ['bisque', 'gold', 'light blue', 'tomato', 'orange', 'olivedrab', 'darkslategray', 'orchid', 'brown', 'navy', 'palegreen']
#CMAP = px.colors.qualitative.Light24




def get_network_new(df, i):
    num_classes = None
    df = df.dropna(subset=[f'TE{i+1}', f'seTE{i+1}'])
    # print(df.columns)
    treat1_class = "treat_class1"
    treat2_class = "treat_class2"

    if treat1_class and treat2_class in df.columns:
        df_treat = df.treat1.dropna().append(df.treat2.dropna()).reset_index(drop=True)
        df_class = df.treat_class1.dropna().append(df.treat_class2.dropna()).reset_index(drop=True)
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
    all_nodes_sized = pd.concat([all_nodes_sized, all_nodes_robs], axis=1).reset_index() if not df_n1g.rob.value_counts().empty else all_nodes_sized.reset_index()

    if treat1_class and treat2_class in df.columns: all_nodes_sized = pd.concat([all_nodes_sized, all_nodes_class['class']], axis=1).reset_index(drop=True)

    if not df_n1g.rob.value_counts().empty:
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

    if treat1_class and treat2_class in df.columns:
        if not df_n1g.rob.value_counts().empty:
            cy_nodes = [{"data": {"id": target,
                                    "label": target,
                                    "n_class": num_classes,
                                #   'size': np.power(size,1/4)*8 / (max_trsfrmd_size_nodes-node_size),
                                    'size': n2,
                                    'pie1': r1 / (r1 + r2 + r3) if not r1 + r2 + r3 == 0 else None,
                                    'pie2': r2 / (r1 + r2 + r3) if not r1 + r2 + r3 == 0 else None,
                                    'pie3': r3 / (r1 + r2 + r3) if not r1 + r2 + r3 == 0 else None,
                                    },'classes': f'{CMAP[cls]}'} for target, size, r1, r2, r3, cls,n2 in all_nodes_sized.values]
        else:
            cy_nodes = [{"data": {"id": target,
                                    "label": target,
                                    "n_class": num_classes,
                                #   'size': np.power(size,1/4)*8 / (max_trsfrmd_size_nodes-node_size),
                                    'size': n2,
                                    },'classes': f'{CMAP[cls]}'} for target, size, cls,n2 in all_nodes_sized.values]
    else:
        if not df_n1g.rob.value_counts().empty:
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
        else:
            cy_nodes = [{"data": {"id": target,
                                    "label": target,
                                    'classes': 'genesis',
                                    'size': n2,},
                                    } for
                        target, size, n2 in all_nodes_sized.values]

    return cy_edges + cy_nodes





## ---------------------------  Parse DATA  -------------------------------- ##

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    missing_values = ["n/a", "na", "--", '.', 'missing', 'NA', 'NAN', 'None', '', ' ']
    if 'csv' in filename:  # Assume that the user uploaded a CSV file
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8', errors = 'ignore')), na_values = missing_values)
        except:
            try:
                df = pd.read_csv(io.StringIO(decoded.decode('unicode-escape',errors ='ignore')), na_values = missing_values)
            except:
                df = pd.read_csv(io.StringIO(decoded.decode('ISO-8859-1')))
        return df
    elif 'xls' in filename:  # TODO: add xls options: so far this is not working
        return pd.read_excel(io.BytesIO(decoded))


## ----------------------  Reshape pd data from long to wide  --------------------------- ##

# def adjust_data(data, value_format, value_outcome2):
#     data['rob'] = data['rob'].astype("string")
#     data['rob'] = (data['rob'].str.lower()
#                       .str.strip()
#                       .replace({'low': 'l', 'medium': 'm', 'high': 'h'})
#                       .replace({'l': 1, 'm': 2, 'h': 3}))

#     if value_format=='long':
#         if is_numeric_dtype(data['treat']):
#             data['treat'] = data['treat'].astype(str) + '_'
#         try:
#             for c in data.columns:
#                 if data[c].dtype == object:
#                     data[c].fillna('__NONE__', inplace=True)
#         except:
#             pass
#         if value_outcome2:
#             data = apply_r_func_two_outcomes(func=run_pairwise_data_long_r, df=data)
#         else:

#             data = apply_r_func(func=run_pairwise_data_long_r, df=data)
#         data[data=='__NONE__'] = np.nan
#     if value_format=='contrast':
#         for c in data.columns:
#             if data[c].dtype == object:
#                 data[c].fillna('__NONE__', inplace=True)
#         if value_outcome2:
#             data = apply_r_func_two_outcomes(func=run_pairwise_data_contrast_r, df=data)
#         else:
#             data = apply_r_func(func=run_pairwise_data_contrast_r, df=data)
#         data[data=='__NONE__'] = np.nan

#     if value_format == 'iv':
#         data = data
#         if value_outcome2:
#             data = data
#     return data


def adjust_data(data, value_format, number_outcomes):
    
    data['rob'] = data['rob'].astype("string")
    data['rob'] = (data['rob'].str.lower()
                    .str.strip()
                    .replace({'low': 'l', 'medium': 'm', 'high': 'h'})
                    .replace({'l': 1, 'm': 2, 'h': 3}))

    if value_format=='long':
        if is_numeric_dtype(data['treat']):
            data['treat'] = data['treat'].astype(str) + '_'
        try:
            for c in data.columns:
                if data[c].dtype == object:
                    data[c].fillna('__NONE__', inplace=True)
        except:
            pass
        
        data = apply_r_func_two_outcomes(func=run_pairwise_data_long_r, df=data, num_outcomes = number_outcomes)
       
        data[data=='__NONE__'] = np.nan
    if value_format=='contrast':
        for c in data.columns:
            if data[c].dtype == object:
                data[c].fillna('__NONE__', inplace=True)
        
        data = apply_r_func_two_outcomes(func=run_pairwise_data_contrast_r, df=data, num_outcomes = number_outcomes)
        
        data[data=='__NONE__'] = np.nan

    if value_format == 'iv':
        data = data
    return data





## ----------------------  FUNCTIONS for Running data analysis in R  --------------------------- ##

def data_checks(df, num_outcomes):
    # df = df.infer_objects()
    # types = df.applymap(type).apply(set)
    # types_sets = types[types.apply(len) > 1]
    indict3 = 0
    
    # for i in range(int(num_outcomes)):
    #     if df[f'seTE{i+1}'] > 0:
    #         indict3 += 1 
        
    return {
         #   'Some columns contain a mix of string and numeric characters. This can create issues in data tables. Please use numbers (with decimal separator for floats) for a numeric variable': len(types_sets) > 0,
            'Some variables are a mix of numerical and string values. This can create issues in data tables. Please use numerical (decimal sep for floats)': all(df.applymap(type).nunique() > 1),
            'Missing values present': df.isnull().sum().sum() < 1,
            'Negative variances present': df.isnull().sum().sum() < 1

            }


## run netmeta for nma forest plots
def run_network_meta_analysis(df,i):
    data_forest = apply_r_func_new(func=run_NetMeta_r, df=df, i=i)
    return data_forest




## run metagen for pairwise forest plots
def run_pairwise_MA(df,i):
    forest_MA = apply_r_func_new(func=pairwise_forest_r, df=df, i=i)
    return forest_MA


## run netmeta for league table, consistency tables and ranking plots
# def generate_league_table(df, outcome2=False):

#     if outcome2: leaguetable, pscores, consist, netsplit, netsplit2, netsplit_all, netsplit_all2  = apply_r_func_two_outcomes(func=league_table_r, df=df)
#     else:        leaguetable, pscores, consist, netsplit, netsplit_all = apply_r_func(func=league_table_r, df=df)

#     replace_and_strip = lambda x: x.replace(' (', '\n(').strip()

#     leaguetable = leaguetable.fillna('')

#     leaguetable = pd.DataFrame([[replace_and_strip(col) for col in list(row)] for idx, row in leaguetable.iterrows()],
#                                columns=leaguetable.columns,
#                                index=leaguetable.index)

#     leaguetable.columns = leaguetable.index = leaguetable.values.diagonal()

#     if outcome2:
#         return leaguetable, pscores, consist, netsplit, netsplit2, netsplit_all, netsplit_all2
#     else:
#         return leaguetable, pscores, consist, netsplit, netsplit_all
def generate_league_table(df, i):
    
    leaguetable, pscores, consist, netsplit, netsplit_all = apply_r_func_new(func=league_table_r, df=df, i =i)

    replace_and_strip = lambda x: x.replace(' (', '\n(').strip()

    leaguetable = leaguetable.fillna('')

    leaguetable = pd.DataFrame([[replace_and_strip(col) for col in list(row)] for idx, row in leaguetable.iterrows()],
                               columns=leaguetable.columns,
                               index=leaguetable.index)

    leaguetable.columns = leaguetable.index = leaguetable.values.diagonal()

    
    return leaguetable, pscores, consist, netsplit, netsplit_all


def generate_league_table_both(df, i, j):
    
    leaguetable = apply_r_func_new_lt(func=league_table_r_both, df=df, i =i, j=j)
    replace_and_strip = lambda x: x.replace(' (', '\n(').strip()

    leaguetable = leaguetable.fillna('')

    leaguetable = pd.DataFrame([[replace_and_strip(col) for col in list(row)] for idx, row in leaguetable.iterrows()],
                               columns=leaguetable.columns,
                               index=leaguetable.index)

    leaguetable.columns = leaguetable.index = leaguetable.values.diagonal()

    
    return leaguetable




## run netmeta for funnel plots
def generate_funnel_data(df,i):
    funnel = apply_r_func_new(func=funnel_plot_r,df=df, i=i)
    return funnel


def create_sessions_folders():
    for dir in [__TEMP_LOGS_AND_GLOBALS, __SESSIONS_FOLDER, __TEMP_LOGS_AND_GLOBALS]:
        if not os.path.exists(dir):
            os.makedirs(dir)
        # os.makedirs(__TEMP_LOGS_AND_GLOBALS, exist_ok=True)


def clean_sessions_folders():
    """Deletes all folders in __temp_logs_and_globals (__TEMP_LOGS_AND_GLOBALS)
    created more than 2 days ago."""
    del_folders = [p for p in os.listdir(__TEMP_LOGS_AND_GLOBALS)
                   if p[0]!='.' and p<YESTERDAY]
    for dir in del_folders:
        shutil.rmtree(f'{__TEMP_LOGS_AND_GLOBALS}/{dir}', ignore_errors=True)



