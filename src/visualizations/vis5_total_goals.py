import plotly.express as px

def draw_figure(sorted_goals):
    top_matches = sorted_goals.head(10)

    fig = px.bar(top_matches, 
                x='TotalGoals', 
                y=top_matches.apply(lambda row: f"{row['HomeTeamName']} vs {row['AwayTeamName']}", axis=1), 
                orientation='h', 
                title='Top EURO 2020 Matches by Total Goals Scored',
                labels={'TotalGoals': 'Total Goals', 'y': 'Match'},
                height=600,
                color='TotalGoals',
                color_continuous_scale='Blues',
                )
    fig.update_layout(
        plot_bgcolor='#d2f6f6',
        paper_bgcolor='#d2f6f6',
    )
    return fig