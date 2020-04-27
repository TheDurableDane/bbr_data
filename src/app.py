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


def prepare_data(data):
    data['year'] = data['sold_date'].dt.year
    data['quarter'] = data['sold_date'].dt.quarter
    data['quarter'] = data['year'] + data['quarter']/10*2.5
    data['month'] = data['sold_date'].dt.month
    data['month'] = data['year'] + data['month']/10/1.2
    data = data.query('year >= 1992')
    data = data.query('price_change <= 500')
    data['price_change'] = data['price_change']/100

    conditions = [
        ((data['zip_code'].values >= 1000) & (data['zip_code'].values < 2000)),
        ((data['zip_code'].values >= 2000) & (data['zip_code'].values < 3000)),
        ((data['zip_code'].values >= 3000) & (data['zip_code'].values < 4000)),
        ((data['zip_code'].values >= 4000) & (data['zip_code'].values < 5000)),
        ((data['zip_code'].values >= 5000) & (data['zip_code'].values < 6000)),
        ((data['zip_code'].values >= 6000) & (data['zip_code'].values < 7000)),
        ((data['zip_code'].values >= 7000) & (data['zip_code'].values < 8000)),
        ((data['zip_code'].values >= 8000) & (data['zip_code'].values < 9000)),
        ((data['zip_code'].values >= 9000) & (data['zip_code'].values < 10000)),
    ]
    categories = ['1000-1999', '2000-2999', '3000-3999', '4000-4999', '5000-5999', '6000-6999', '7000-7999', '8000-8999', '9000-9999']
    data['zip_code_group'] = np.select(conditions, categories, default='Unknown')

    conditions = [
        ((data['zip_code'].values >= 1000) & (data['zip_code'].values < 5000)),
        ((data['zip_code'].values >= 5000) & (data['zip_code'].values < 6000)),
        ((data['zip_code'].values >= 6000) & (data['zip_code'].values < 10000)),
    ]
    categories = ['Sjælland', 'Fyn', 'Jylland']
    data['region'] = np.select(conditions, categories, default='Unknown')

    return data


def prepare_histogram_data(data):
    data['year'] = data['sold_date'].dt.year
    data = data.query('year >= 1992')
    data = data.query('price_change <= 20')
    data = data.query('rooms < 60')

    return data


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
                        tooltip={'always_visible': True, 'placement': 'bottom'},
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
        html.Br(),
        dcc.Dropdown(id='geo_dropdown',
                     options=[
                         {'label': 'Price', 'value': 'price'},
                         {'label': 'Rooms', 'value': 'rooms'},
                         {'label': 'Residence Size', 'value': 'residence_size'}
                     ],
                     value='price',
                     clearable=False),
        html.Br(),
        html.P('Sold date'),
        dcc.Slider(id='geo_year_slider',
                   min=1992,
                   max=2020,
                   step=1,
                   value=2020,
                   included=False,
                   tooltip={'always_visible': True, 'placement': 'bottom'})]),
    dbc.Col(width=10, children=[
        dcc.Graph(id='geo_map')
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
                     clearable=False),
        html.Br(),
        dcc.Dropdown(id='timeseries_dropdown',
                     options=[
                         {'label': 'Price', 'value': 'price'},
                         {'label': 'Price Change', 'value': 'price_change'},
                         {'label': 'Rooms', 'value': 'rooms'},
                         {'label': 'Residence Size', 'value': 'residence_size'}
                     ],
                     value='price',
                     clearable=False),
        html.Br(),
        html.P('Split by:'),
        dcc.RadioItems(id='timeseries_split_by',
                       options=[
                           {'label': 'None', 'value': 'none'},
                           {'label': 'Zip code', 'value': 'zip_code_group'},
                           {'label': 'Region', 'value': 'region'}
                       ],
                       value='none',
                       labelStyle={'display': 'block'}),
        html.Br(),
        html.P('Resolution:'),
        dcc.RadioItems(id='timeseries_resolution',
                       options=[
                           {'label': 'Year', 'value': 'year'},
                           {'label': 'Quarter', 'value': 'quarter'},
                           {'label': 'Month', 'value': 'month'}
                       ],
                       value='year',
                       labelStyle={'display': 'block'})
    ]),
    dbc.Col(width=10, children=[
        dcc.Graph(id='timeseries')
    ])
])


app.layout = dbc.Row([
    dbc.Col(width={'size': 6, 'offset': 3}, children=[
        dbc.Tabs([
            dbc.Tab(label='Geography', children=tab_geography),
            dbc.Tab(label='Time series', children=tab_timeseries),
            dbc.Tab(label='Histograms', children=tab_histograms),
        ])
    ])
])


@app.callback(
    Output('histogram', 'figure'),
    [Input('hist_dropdown', 'value'),
     Input('hist_range_slider', 'value'),
     Input('hist_checklist', 'value')])
def update_histogram(hist_dropdown, hist_range_slider, hist_checklist):
    data_to_plot = prepare_histogram_data(data)
    slider_min = hist_range_slider[0]
    slider_max = hist_range_slider[1]

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
        template='simple_white',
        uirevision=hist_dropdown)

    return fig


@app.callback(
    Output('timeseries', 'figure'),
    [Input('timeseries_dropdown', 'value'),
     Input('timeseries_dropdown_calc', 'value'),
     Input('timeseries_split_by', 'value'),
     Input('timeseries_resolution', 'value')])
def update_timeseries(timeseries_dropdown, timeseries_dropdown_calc, timeseries_split_by, timeseries_resolution):
    data_to_plot = prepare_data(data)
    ylabel = ' '.join(timeseries_dropdown.split('_')).title()

    if timeseries_split_by == 'none':
        n_sales_per_time = data_to_plot.groupby(timeseries_resolution).size().reset_index(name='count')

        if timeseries_dropdown_calc == 'mean':
            data_to_plot = data_to_plot.groupby(timeseries_resolution)[timeseries_dropdown].mean().reset_index()
        elif timeseries_dropdown_calc == 'median':
            data_to_plot = data_to_plot.groupby(timeseries_resolution)[timeseries_dropdown].median().reset_index()

        line_color = '#d62728'
        line_plot = go.Scatter(x=data_to_plot[timeseries_resolution], y=data_to_plot[timeseries_dropdown], yaxis='y2', line_color=line_color)
        bar_color = '#1f77b4'
        sales_per_time_plot = go.Bar(x=n_sales_per_time[timeseries_resolution], y=n_sales_per_time['count'], marker_color=bar_color)
        fig = go.Figure(data=[sales_per_time_plot, line_plot],
                        layout=go.Layout(
                             yaxis=dict(
                                 title='Number of sales',
                                 side='right',
                                 color=bar_color
                             ),
                             yaxis2=dict(
                                 title=ylabel,
                                 overlaying='y',
                                 side='left',
                                 color=line_color
                             )
                         )
        )
        fig.update_layout(showlegend=False)

    else:
        if timeseries_dropdown_calc == 'mean':
            data_to_plot = data_to_plot.groupby([timeseries_resolution, timeseries_split_by])[timeseries_dropdown].mean().reset_index()
        elif timeseries_dropdown_calc == 'median':
            data_to_plot = data_to_plot.groupby([timeseries_resolution, timeseries_split_by])[timeseries_dropdown].median().reset_index()

        fig = px.line(data_to_plot, x=timeseries_resolution, y=timeseries_dropdown, color=timeseries_split_by)\
                .for_each_trace(lambda t: t.update(name=t.name.replace(timeseries_split_by + '=', '')))
        fig.update_layout(yaxis_title=ylabel)

    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=np.arange(1992, 2021),
            ticktext=np.arange(1992, 2021)),
        xaxis_title='Time',
        template='simple_white',
        uirevision=timeseries_dropdown)

    if timeseries_dropdown == 'price_change':
        fig.update_layout(yaxis2_tickformat='%')

    return fig


@app.callback(
    Output('geo_map', 'figure'),
    [Input('geo_dropdown', 'value'),
     Input('geo_year_slider', 'value')])
def update_map(geo_dropdown, geo_dropdown_calc, geo_year_slider):
    pass

# return fig


if __name__ == '__main__':
    app.run_server(debug=True)
