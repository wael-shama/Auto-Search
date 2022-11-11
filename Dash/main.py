import glob
import sys

from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
from dash import dash_table, callback, Output, Input

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
#

link_col = "link"
def link_format(x, target_col=5):
    return "[{}]({})".format('ebay link', x[link_col])

def read_csv_files(dir_path):
    extension = 'csv'
    all_filenames = [i for i in glob.glob('{}/*.{}'.format(dir_path, extension))]
    # combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    # export to csv
    return combined_csv

def table_type(df_column):
    if isinstance(df_column.dtype, pd.DatetimeTZDtype):
        return 'datetime',
    elif (is_string_dtype(df_column) or
          isinstance(df_column.dtype, pd.StringDtype) or
            isinstance(df_column.dtype, pd.BooleanDtype) or
            isinstance(df_column.dtype, pd.CategoricalDtype) or
            isinstance(df_column.dtype, pd.PeriodDtype)):
        return 'text'
    elif (is_numeric_dtype(df_column) or
          isinstance(df_column.dtype, pd.SparseDtype) or
            isinstance(df_column.dtype, pd.IntervalDtype) or
            isinstance(df_column.dtype, pd.Int8Dtype) or
            isinstance(df_column.dtype, pd.Int16Dtype) or
            isinstance(df_column.dtype, pd.Int32Dtype) or
            isinstance(df_column.dtype, pd.Int64Dtype)):
        return 'numeric'
    else:
        return 'any'


df = read_csv_files(dir_path=r"./output")
df[link_col] = df.apply(lambda x: link_format(x, link_col), axis=1)




dropdown = dbc.Row(
    [
        dbc.Col(
            dcc.Dropdown(
                ['New York City', 'Montreal', 'San Francisco'],
                ['Montreal', 'San Francisco'],
                multi=True
            )
        ),

    ]
)

app.layout = dbc.Container(
    children=[
        dropdown,
        dbc.Container([
            dbc.Label('Click a cell in the table:'),
            dash_table.DataTable(df.to_dict('records'),
                                 [{"name": i, "id": i, 'presentation': 'markdown', 'type': table_type(df[i])} if i == 'link'else {"name": i, "id": i, 'type': table_type(df[i])} for i in df.columns],
                                 id='tbl',
filter_action="native",
sort_action="native",
                                style_cell={
                                'textAlign': 'left',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis',
                                        'maxWidth': 0,
                                    },
                            style_cell_conditional=[
                                    {'if': {'column_id': 'year'},
                                     'width': '{}%'.format(len(df.columns))},
                                {'if': {'column_id': 'published_date'},
                                 'width': '{}%'.format(len(df.columns)*2)}
                            ],
                                 tooltip_data=[
                                     {
                                         column: {'value': str(value), 'type': 'markdown'}
                                         for column, value in row.items()
                                     } for row in df.to_dict('records')
                                 ],
                                 tooltip_duration=None,
                                 style_data={
                                     'color': 'black',
                                     'backgroundColor': 'white'
                                 },
                                 style_data_conditional=[
                                     {
                                         'if': {'row_index': 'odd'},
                                         'backgroundColor': 'rgb(220, 220, 220)',
                                     }
                                 ],
                                 style_header={
                                     'backgroundColor': 'rgb(210, 210, 210)',
                                     'color': 'black',
                                     'fontWeight': 'bold'
                                 }
                                 ),
            dbc.Alert(id='tbl_out'),
        ])
    ])


@callback(Output('tbl_out', 'children'), Input('tbl', 'active_cell'))
def update_graphs(active_cell):
    return str(active_cell) if active_cell else "Click the table"


if __name__ == '__main__':

    app.run_server(host='127.0.0.1', debug=True)
