import plotly.express as px

def draw_figure(outcome_percentage):
    # filter top 10 matches by total goals
    fig = px.pie(
        values=outcome_percentage,
        names=outcome_percentage.index,
        title='Percentage of EURO 2020 Matches Outcome for Home Team',
        hole=0.3
)
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Percentage: %{percent}',
        )
    fig.update_layout(
        legend=dict(
            itemclick=False,
            itemdoubleclick=False
        )
    )
    return fig