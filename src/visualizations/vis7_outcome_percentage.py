import plotly.express as px

def draw_figure(outcome_percentage):

    darker_blue_colors = px.colors.sequential.Blues_r

    fig = px.pie(
        values=outcome_percentage,
        names=outcome_percentage.index,
        title='Percentage of EURO 2020 Matches Outcome for Home Team',
        hole=0.3,
        color_discrete_sequence=darker_blue_colors

)
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Percentage: %{percent}',
        )
    fig.update_layout(
        legend=dict(
            itemclick=False,
            itemdoubleclick=False
        ),
        plot_bgcolor='#d2f6f6',
        paper_bgcolor='#d2f6f6',
    )
    return fig