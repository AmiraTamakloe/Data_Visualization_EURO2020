
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
from visualizations.vis4 import vis4_goal_diff
from visualizations.vis5 import vis5_total_goals

app = dash.Dash(__name__)
app.title = 'Euro2020 - INF8808 - Amira Tamakloe'

def prep_data_vis4():
    '''
        Imports the .csv file and does some preprocessing.

        Returns:
            A pandas dataframe containing the preprocessed data.
    '''
    df = pd.read_csv('./src/assets/data/project_data.csv')
    df_filtered  = preprocess.drop_useless_columns(df)
    match_df = preprocess.get_statistics(df_filtered)

    return match_df

def prep_data_vis5():
    df_match_info = pd.read_csv('./src/assets/data/project_data.csv')
    sorted_goals = preprocess.vis5_get_total_goals(df_match_info)
    goals_df = vis5_total_goals.draw_figure(sorted_goals)

    return goals_df


# TODO: add 5-6 parameters for this function
def init_app_layout(vis4_goals, vis5_goals):
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
                    figure=vis4_goals,
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
            ]),
            # todo: add kids
            html.Div(className='viz-container', children=[
                dcc.Graph(
                    figure=vis5_goals,
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
            ]),
        ]),
    ])


# DATA PREP:


# VIS 4
vis4_data_bar_chart = prep_data_vis4()
fig4 = vis4_goal_diff.init_figure()
print(fig4)
fig4 = vis4_goal_diff.draw(fig4, vis4_data_bar_chart)

# VIS 5
fig5 = prep_data_vis5()

# TOTAL LAYOUT
app.layout = init_app_layout(fig4, fig5)
