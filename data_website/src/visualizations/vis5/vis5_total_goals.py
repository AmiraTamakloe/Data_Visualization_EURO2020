import pandas as pd
import plotly.express as px



def draw_figure(sorted_goals):
    # filter top 10 matches by total goals
    top_matches = sorted_goals.head(10)

    fig = px.bar(top_matches, 
                x='TotalGoals', 
                y=top_matches.apply(lambda row: f"{row['HomeTeamName']} vs {row['AwayTeamName']}", axis=1), 
                orientation='h', 
                title='Top EURO 2020 Matches by Total Goals Scored',
                labels={'TotalGoals': 'Total Goals', 'y': 'Match'},
                height=600)

    return fig