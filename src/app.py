#!/usr/bin/env python
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import database_functions as dbf


data = dbf.read_house_price_data('../data/bbr.db')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


tab_histograms = dbc.Row([
    dbc.Col(width={"size": 2}, children=[
        dcc.Dropdown(id='hist_data',
            options=[
                {'label': 'Price', 'value': 'price'},
                {'label': 'Rooms', 'value': 'rooms'},
                {'label': 'Residence size', 'value': 'residence_size'}
            ],
            value='price',
            clearable=False
        )
    ]),
    dbc.Col(width=10, children=[
        dcc.Graph(id='histogram')
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


@app.callback(
    Output(component_id='histogram', component_property='figure'),
    [Input(component_id='hist_data', component_property='value')])
def update_histogram(histogram_dropdown_value):
    fig = px.histogram(data, x=histogram_dropdown_value)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
