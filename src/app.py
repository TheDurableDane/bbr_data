#!/usr/bin/env python
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import database_functions as dbf


data = dbf.read_house_price_data('../data/bbr.db')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


tab_histograms = dbc.Row([
    dbc.Col(width={'size': 2}, children=[
        html.Br(),
        dcc.Dropdown(id='hist_dropdown',
                     options=[
                         {'label': 'Price', 'value': 'price'},
                         {'label': 'Rooms', 'value': 'rooms'},
                         {'label': 'Residence Size', 'value': 'residence_size'}
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
    dbc.Col(width={'size': 2}, children=[
    ]),
    dbc.Col(width=10, children=[
        html.P('Graphs and content.')
    ])
])


tab_timeseries = dbc.Row([
    dbc.Col(width={'size': 2}, children=[
        html.Br(),
        dcc.Dropdown(id='timeseries_dropdown_calc',
                     options=[
                         {'label': 'Mean', 'value': 'mean'},
                         {'label': 'Median', 'value': 'median'}
                     ],
                     value='mean',
                     clearable=False
        ),
        html.Br(),
        dcc.Dropdown(id='timeseries_dropdown',
                     options=[
                         {'label': 'Price', 'value': 'price'},
                         {'label': 'Rooms', 'value': 'rooms'},
                         {'label': 'Residence Size', 'value': 'residence_size'}
                     ],
                     value='price',
                     clearable=False
        ),
        html.Br(),
        html.P('Split by:'),
        dcc.RadioItems(id='timeseries_split_by',
                       options=[
                           {'label': 'None', 'value': 'none'},
                           {'label': 'Zip code', 'value': 'zip_code'},
                           {'label': 'Jylland/Fyn/Sjælland', 'value': 'jfs'}
                       ],
                       value='zip_code',
                       labelStyle={'display': 'block'})
    ]),
    dbc.Col(width=10 , children=[
        dcc.Graph(id='timeseries')
    ])
])


app.layout = dbc.Row([
    dbc.Col(width={'size': 6, 'offset': 3}, children=[
        dbc.Tabs([
            dbc.Tab(label='Histograms', children=tab_histograms),
            dbc.Tab(label='Geography', children=tab_geography),
            dbc.Tab(label='Time series', children=tab_timeseries),
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


@app.callback(
    Output('timeseries', 'figure'),
    [Input('timeseries_dropdown', 'value'),
     Input('timeseries_dropdown_calc', 'value'),
     Input('timeseries_split_by', 'value')])
def update_timeseries(timeseries_dropdown, timeseries_dropdown_calc, timeseries_split_by):
    data_to_plot = data.copy()
    data_to_plot['year'] = data_to_plot['sold_date'].dt.year
    data_to_plot = data_to_plot.query('year >= 1992')

    if timeseries_split_by == 'zip_code':
        conditions = [
            ((data_to_plot['zip_code'].values >= 1000) & (data_to_plot['zip_code'].values < 2000)),
            ((data_to_plot['zip_code'].values >= 2000) & (data_to_plot['zip_code'].values < 3000)),
            ((data_to_plot['zip_code'].values >= 3000) & (data_to_plot['zip_code'].values < 4000)),
            ((data_to_plot['zip_code'].values >= 4000) & (data_to_plot['zip_code'].values < 5000)),
            ((data_to_plot['zip_code'].values >= 5000) & (data_to_plot['zip_code'].values < 6000)),
            ((data_to_plot['zip_code'].values >= 6000) & (data_to_plot['zip_code'].values < 7000)),
            ((data_to_plot['zip_code'].values >= 7000) & (data_to_plot['zip_code'].values < 8000)),
            ((data_to_plot['zip_code'].values >= 8000) & (data_to_plot['zip_code'].values < 9000)),
            ((data_to_plot['zip_code'].values >= 9000) & (data_to_plot['zip_code'].values < 10000)),
        ]
        categories = ['1000-1999', '2000-2999', '3000-3999', '4000-4999', '5000-5999', '6000-6999', '7000-7999', '8000-8999', '9000-9999']
        data_to_plot['split_by'] = np.select(conditions, categories, default='Unknown')
    elif timeseries_split_by == 'jfs':
        conditions = [
            ((data_to_plot['zip_code'].values >= 1000) & (data_to_plot['zip_code'].values < 5000)),
            ((data_to_plot['zip_code'].values >= 5000) & (data_to_plot['zip_code'].values < 6000)),
            ((data_to_plot['zip_code'].values >= 6000) & (data_to_plot['zip_code'].values < 10000)),
        ]
        categories = ['Sjælland', 'Fyn', 'Jylland']
        data_to_plot['split_by'] = np.select(conditions, categories, default='Unknown')

    if timeseries_split_by == 'none':
        if timeseries_dropdown_calc == 'mean':
            data_to_plot = data_to_plot.groupby('year')[timeseries_dropdown].mean().reset_index()
        elif timeseries_dropdown_calc == 'median':
            data_to_plot = data_to_plot.groupby('year')[timeseries_dropdown].median().reset_index()

        fig = px.line(data_to_plot, x='year', y=timeseries_dropdown)
    else:
        if timeseries_dropdown_calc == 'mean':
            data_to_plot = data_to_plot.groupby(['year', 'split_by'])[timeseries_dropdown].mean().reset_index()
        elif timeseries_dropdown_calc == 'median':
            data_to_plot = data_to_plot.groupby(['year', 'split_by'])[timeseries_dropdown].median().reset_index()

        fig = px.line(data_to_plot, x='year', y=timeseries_dropdown, color='split_by')\
                .for_each_trace(lambda t: t.update(name=t.name.replace('split_by=','')))

    ylabel = ' '.join(timeseries_dropdown.split('_')).title()
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title=ylabel,)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
