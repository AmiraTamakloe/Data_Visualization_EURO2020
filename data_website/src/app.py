
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Amira Tamakloe
    Course: INF8808
    Python Version: 3.8
'''

import dash
from dash import html
from dash import dcc


import pandas as pd
import preprocess
import bar_chart

app = dash.Dash(__name__)
app.title = 'Euro2020 - INF8808 - Amira Tamakloe'

def prep_data():
    '''
        Imports the .csv file and does some preprocessing.

        Returns:
            A pandas dataframe containing the preprocessed data.
    '''
    df = pd.read_csv('./src/assets/data/project_data.csv')
    df_filtered  = preprocess.drop_useless_columns(df)
    match_df = preprocess.get_statistics(df_filtered)

    return match_df


def init_app_layout(figure):
    '''
        Generates the HTML layout representing the app.

        Args:
            figure: The figure to display.
        Returns:
            The HTML structure of the app's web page.
    '''
    return html.Div(className='content', children=[
        html.Header(children=[
            html.H1('Euro 2020 Data Analysis'),
        ]),
        html.Main(children=[
            html.Div(className='viz-container', children=[
                dcc.Graph(
                    figure=figure,
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    ),
                    className='graph',
                    id='line-chart'
                )
            ])
        ]),
    ])



data = prep_data()
fig = bar_chart.init_figure()
print(fig)
fig = bar_chart.draw(fig, data)
app.layout = init_app_layout(fig)
