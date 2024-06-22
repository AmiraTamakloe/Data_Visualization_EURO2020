


import pandas as pd
import plotly.graph_objects as go

def MakeItalic(win_loss_record: pd.DataFrame) -> list:
    italic_country_names = [f'<i>{country}</i>' for country in win_loss_record.index]
    return italic_country_names

def DrawBarChart(italic_country_names: list, win_loss_record: pd.DataFrame) -> go.Figure:
    # Create the bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=italic_country_names,
        y=win_loss_record['Wins'],
        name='Wins',
        marker_color='rgb(99, 110, 250)'
    ))

    fig.add_trace(go.Bar(
        x=italic_country_names,
        y=win_loss_record['Losses'],
        name='Losses',
        marker_color='rgb(239, 85, 59)'
    ))

    fig.update_layout(
        title={
            'text': 'Win-Loss Record of Teams in EURO 2020',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis=dict(
            title='Country',
            titlefont=dict(size=16),
            tickfont_size=14,
        ),
        yaxis=dict(
            title='Number of Matches',
            titlefont=dict(size=16),
            tickfont_size=14,
        ),
        legend=dict(
            x=1,
            y=0.5,
            traceorder='normal',
            font=dict(
                size=12,
            ),
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.4, # Increase gap between bars of adjacent location coordinates.
        bargroupgap=0.1, # Gap between bars of the same location coordinate.
    )

    return fig