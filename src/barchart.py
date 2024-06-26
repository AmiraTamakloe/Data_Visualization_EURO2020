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
        marker_color='#063970',
        hovertemplate=(
            'Country: %{x}<br>' +
            'Wins: %{y}<br>' +
            '<extra></extra>'
        )
    ))

    fig.add_trace(go.Bar(
        x=italic_country_names,
        y=win_loss_record['Losses'],
        name='Losses',
        marker_color='#2596be',
         hovertemplate=(
            'Country: %{x}<br>' +
            'Losses: %{y}<br>' +
            '<extra></extra>'
        )
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
            bgcolor='#d2f6f6',
            bordercolor='#d2f6f6'
        ),
        barmode='group',
        bargap=0.4,
        bargroupgap=0.1,
        plot_bgcolor='#d2f6f6',
        paper_bgcolor='#d2f6f6',
    )

    return fig
