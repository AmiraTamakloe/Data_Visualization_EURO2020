# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Leila Ekradi
    Course: INF8808
    Python Version: 3.8
'''

import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import preprocess
import bar_chart
import heatmap

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = 'Euro2020 - INF8808 - Leila Ekradi'

def prep_data():
    '''
        Loads and preprocesses the data from the CSV file.
        
        Returns:
            A pandas dataframe containing the preprocessed data.
    '''
    # Load the dataset
    df = pd.read_csv('project_data.csv')
    # Drop unnecessary columns
    df_filtered = preprocess.drop_useless_columns(df)
    # Get match statistics
    match_df = preprocess.get_statistics(df_filtered)
    return match_df

def init_app_layout(bar_chart_fig, heatmap_fig):
    '''
        Initializes the app layout.
        
        Args:
            bar_chart_fig: The bar chart figure to display.
            heatmap_fig: The heatmap figure to display.
        Returns:
            The HTML structure of the app's web page.
    '''
    return html.Div(className='content', children=[
        html.Header(children=[
            html.H1('Euro 2020 Data Analysis'),
        ]),
        html.Main(children=[
            html.Div(className='viz-container', children=[
                dcc.Dropdown(
                    id='metric-dropdown',
                    options=[
                        {'label': 'Total Goals', 'value': 'TotalGoals'},
                        {'label': 'Average Goals', 'value': 'AvgGoals'}
                    ],
                    value='TotalGoals',
                    style={'width': '50%'}
                ),
                dcc.Graph(id='performance-bar-chart', figure=bar_chart_fig),
                dcc.Graph(id='team-goals-heatmap', figure=heatmap_fig)
            ])
        ]),
    ])

# Prepare the data
data = prep_data()
# Initialize figures
bar_chart_fig = bar_chart.init_figure()
bar_chart_fig = bar_chart.draw(bar_chart_fig, preprocess.calculate_goals(data))
heatmap_fig = heatmap.draw(data)
# Set the app layout
app.layout = init_app_layout(bar_chart_fig, heatmap_fig)

@app.callback(
    [Output('performance-bar-chart', 'figure'),
     Output('team-goals-heatmap', 'figure')],
    [Input('metric-dropdown', 'value')]
)
def update_graphs(selected_metric):
    '''
        Updates the graphs based on the selected metric.
        
        Args:
            selected_metric: The selected metric from the dropdown.
        Returns:
            Updated bar chart and heatmap figures.
    '''
    df_goals_agg = preprocess.calculate_goals(data)
    bar_chart_fig = bar_chart.update_figure(df_goals_agg, selected_metric)
    heatmap_fig = heatmap.update_figure(data, selected_metric)
    return bar_chart_fig, heatmap_fig

if __name__ == '__main__':
    app.run_server(debug=True)

