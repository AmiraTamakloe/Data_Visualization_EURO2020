import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


def register_callbacks(app, df_goals_agg, df_goals, df_matches_info):

    @app.callback(
        [Output('performance-bar-chart', 'figure'),
        Output('team-goals-heatmap', 'figure')],
        [Input('metric-dropdown', 'value')]
    )
    def update_graphs(selected_metric):
        # Bar chart
        bar_chart_fig = px.bar(df_goals_agg, x='Team', y=selected_metric, color=selected_metric,
                            color_continuous_scale='Blues', title='Team Performance Bar Chart')
        
    
        bar_chart_fig.update_traces(
            hovertemplate='<b>Team: %{x}</b><br>' + 
                        ('Average Goals: %{y:.2f}' if selected_metric == 'AvgGoals' else 'Total Goals: %{y}')
        )
        color_legend_title = 'Average Goals' if selected_metric == 'AvgGoals' else 'Total Goals'
        bar_chart_fig.update_coloraxes(colorbar_title=color_legend_title)

        bar_chart_fig.update_layout(
            xaxis_tickangle=-45,
            plot_bgcolor='#d2f6f6',
            paper_bgcolor='#d2f6f6',
        )
        # Heatmap for total goals or average goals
        if selected_metric == 'TotalGoals':
            heatmap_data = df_goals.pivot(index='Team', columns='MatchNumber', values='Goals').fillna(0)
            color_label = "Total Goals"
        else:
            heatmap_data = df_goals.pivot(index='Team', columns='MatchNumber', values='Goals').fillna(0) / df_goals['MatchNumber'].max()
            color_label = "Average Goals"
        
        heatmap_fig = px.imshow(heatmap_data, 
                                labels=dict(x="Match Number", y="Teams", color=color_label),
                                color_continuous_scale='Blues',
                                title=f'{color_label} per Team per Match')

        #  extracts the home team and away team for each matc
        customdata = []
        for match_number in heatmap_data.columns:
            match_info = df_matches_info[df_matches_info['MatchNumber'] == match_number].iloc[0]
            customdata.append((match_info['HomeTeamName'], match_info['AwayTeamName']))

        
        customdata_matrix = []
        for team in heatmap_data.index:
            customdata_row = []
            for match_number in heatmap_data.columns:
                match = df_goals[(df_goals['Team'] == team) & (df_goals['MatchNumber'] == match_number)]
                if not match.empty:
                    home_team, away_team = customdata[match_number - 1]  
                    if team == home_team:
                        customdata_row.append(f"{home_team} vs {away_team}")
                    else:
                        customdata_row.append(f"{away_team} vs {home_team}")
                else:
                    customdata_row.append(None)
            customdata_matrix.append(customdata_row)

        for trace in heatmap_fig.data:
            trace.customdata = customdata_matrix
            trace.hovertemplate = (
                'Team: %{y}<br>' +
                'Match Number: %{x}<br>' +
                ('Average Goals: %{z:.2f}<br>' if selected_metric == 'AvgGoals' else 'Total Goals: %{z}<br>') +
                'Match: %{customdata}<extra></extra>'
            )

        bar_chart_fig.update_layout(
            height=400,
            autosize=False
        )

        heatmap_fig.update_layout(
            autosize=False,
            height=700,
            margin=dict(l=0, r=0, t=30, b=30),
            xaxis=dict(showgrid=True, gridcolor='black', zeroline=False),
            yaxis=dict(showgrid=True, gridcolor='black', zeroline=False),
            plot_bgcolor='#d2f6f6',
            paper_bgcolor='#d2f6f6',
        )

        return bar_chart_fig, heatmap_fig