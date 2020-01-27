#!/usr/bin/env python
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


tab_histograms = dbc.Row([
    dbc.Col(width={"size": 2, "offset": 3}, children=[
        dbc.DropdownMenu(label='ddm', children=[
            dbc.DropdownMenuItem('item1'),
            dbc.DropdownMenuItem('item2'),
            dbc.DropdownMenuItem('item3')
        ])
    ]),
    dbc.Col(width=4, children=[
        html.P('Graphs and content.')
    ])
])


tab_geography = dbc.Row([
    dbc.Col(width={"size": 2, "offset": 3}, children=[
        dbc.DropdownMenu(label='ddm', children=[
            dbc.DropdownMenuItem('item1'),
            dbc.DropdownMenuItem('item2'),
            dbc.DropdownMenuItem('item3')
        ])
    ]),
    dbc.Col(width=4, children=[
        html.P('Graphs and content.')
    ])
])


tab_timeseries = dbc.Row([
    dbc.Col(width={"size": 2, "offset": 3}, children=[
        dbc.DropdownMenu(label='ddm', children=[
            dbc.DropdownMenuItem('item1'),
            dbc.DropdownMenuItem('item2'),
            dbc.DropdownMenuItem('item3')
        ])
    ]),
    dbc.Col(width=4, children=[
        html.P('Graphs and content.')
    ])
])


app.layout = dbc.Row([
    dbc.Col(width={'size': 6, 'offset': 3}, children=[
        dbc.Tabs([
            dbc.Tab(label='Histograms', children=tab_histograms),
            dbc.Tab(label='Geography', children=tab_geography),
            dbc.Tab(label='Time series', children=tab_timeseries)
        ])
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)
