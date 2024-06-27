import pandas as pd
import plotly.graph_objects as go

def data_processing(DF_Data: pd.DataFrame) -> pd.DataFrame:
    """
    Processes the input DataFrame by dropping duplicate rows based on 'MatchID'
    and keeps the last occurrence of each duplicate.

    Args:
    DF_Data (pd.DataFrame): Input DataFrame to process.

    Returns:
    pd.DataFrame: Processed DataFrame with duplicates removed.
    """
    final_results = DF_Data.drop_duplicates(subset='MatchID', keep='last')
    return final_results

def calculate_win_losses(final_results: pd.DataFrame) -> pd.DataFrame:
    wins = {}
    losses = {}

    for index, row in final_results.iterrows():
        if row['ScoreHome'] > row['ScoreAway']:
            wins[row['HomeTeamName']] = wins.get(row['HomeTeamName'], 0) + 1
            losses[row['AwayTeamName']] = losses.get(row['AwayTeamName'], 0) + 1
        elif row['ScoreHome'] < row['ScoreAway']:
            wins[row['AwayTeamName']] = wins.get(row['AwayTeamName'], 0) + 1
            losses[row['HomeTeamName']] = losses.get(row['HomeTeamName'], 0) + 1
        else:
            continue

    win_loss_record = pd.DataFrame({'Wins': wins, 'Losses': losses}).fillna(0).astype(int)

    win_loss_record['Difference'] = win_loss_record['Wins'] - win_loss_record['Losses']

    win_loss_record = win_loss_record.sort_values(by=['Difference', 'Wins'], ascending=[False, False])
    return win_loss_record

def make_italic(win_loss_record: pd.DataFrame) -> list:
    italic_country_names = [f'<i>{country}</i>' for country in win_loss_record.index]
    return italic_country_names

def draw_bar_chart(italic_country_names: list, win_loss_record: pd.DataFrame) -> go.Figure:
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