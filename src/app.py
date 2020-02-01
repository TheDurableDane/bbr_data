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
        html.Br(),
        dcc.Dropdown(id='hist_data',
                     options=[
                         {'label': 'Price', 'value': 'price'},
                         {'label': 'Rooms', 'value': 'rooms'},
                         {'label': 'Residence size', 'value': 'residence_size'}
                     ],
                     value='price',
                     clearable=False
        ),
        html.Br(),
        html.P('Sold date'),
        dcc.RangeSlider(id='hist_range_slider',
                        min=1992,
                        max=2020,
                        step=1,
                        value=[1992, 2020],
                        tooltip={'always_visible':True, 'placement': 'bottom'},
                        allowCross=False
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
    Output('histogram', 'figure'),
    [Input('hist_data', 'value'),
     Input('hist_range_slider', 'value')])
def update_histogram(histogram_dropdown_value, histogram_range_slider_value):
    slider_min = histogram_range_slider_value[0]
    slider_max = histogram_range_slider_value[1]
    data['year'] = data['sold_date'].dt.year
    data_to_plot = data.query(f'{slider_min} <= year <= {slider_max}')
    xlabel = ' '.join(histogram_dropdown_value.split('_')).title()

    fig = px.histogram(data_to_plot, x=histogram_dropdown_value)
    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title='')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
