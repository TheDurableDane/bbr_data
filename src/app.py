#!/usr/bin/env python
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go

import database_functions as dbf


data = dbf.read_house_price_data('../data/bbr.db')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


tab_histograms = dbc.Row([
    dbc.Col(width={"size": 2}, children=[
        html.Br(),
        dcc.Dropdown(id='hist_dropdown',
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
        ),
        html.Br(),
        html.Br(),
        dcc.Checklist(id='hist_checklist',
            options=[
                {'label': 'Jylland', 'value': 'jylland'},
                {'label': 'Fyn', 'value': 'fyn'},
                {'label': 'Sjælland', 'value': 'sjaelland'}
            ],
            value=['jylland', 'fyn', 'sjaelland'],
            labelStyle={'display': 'block'})
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
    [Input('hist_dropdown', 'value'),
     Input('hist_range_slider', 'value'),
     Input('hist_checklist', 'value')])
def update_histogram(hist_dropdown, hist_range_slider, hist_checklist):
    slider_min = hist_range_slider[0]
    slider_max = hist_range_slider[1]

    data_to_plot = data.copy()
    if 'sjaelland' not in hist_checklist:
        checklist_query = 'zip_code > 4999'
        data_to_plot = data_to_plot.query(checklist_query)
    if 'fyn' not in hist_checklist:
        checklist_query = 'zip_code < 5000 or zip_code > 5999'
        data_to_plot = data_to_plot.query(checklist_query)
    if 'jylland' not in hist_checklist:
        checklist_query = 'zip_code < 6000'
        data_to_plot = data_to_plot.query(checklist_query)

    data_to_plot['year'] = data['sold_date'].dt.year
    slider_query = f'{slider_min} <= year <= {slider_max}'
    data_to_plot = data_to_plot.query(slider_query)

    data_median = data_to_plot.loc[:, hist_dropdown].median()

    fig = px.histogram(data_to_plot, x=hist_dropdown)
    fig.add_shape(
        go.layout.Shape(
            type='line',
            xref='x',
            yref='paper',
            x0=data_median,
            y0=0,
            x1=data_median,
            y1=1,
            line=dict(color='red', width=2)
        )
    )

    xlabel = ' '.join(hist_dropdown.split('_')).title()
    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title='Count',
        showlegend=True)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
