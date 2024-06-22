import plotly.express as px

def draw_figure(outcome_percentage):
    # filter top 10 matches by total goals
    fig = px.pie(
        values=outcome_percentage,
        names=outcome_percentage.index,
        title='Percentage of EURO 2020 Matches Outcome for Home Team',
        labels={'label': 'Outcome', 'value': 'Percentage'},
        hole=0.3
)

    return fig