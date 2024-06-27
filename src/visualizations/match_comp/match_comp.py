import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio


from plotly.subplots import make_subplots
import pandas as pd





# create a side bar for first column
SIDEBAR_STYLE = {
    # "position": "fixed",
    # "top": 0,
    # "left": 0,
    # "bottom": 0,
    # "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

def create_sidebar_layout(df):
    sidebar = html.Div(
    [
        html.H2("Match Strategies Comparison"),
        html.Hr(),
        html.P(
            "Game Round:", className="lead"
        ),
        dbc.Nav(
            [
                dcc.Dropdown(
                id='roundname-dropdown',
                options=[{'label': roundname.capitalize(), 'value': roundname} for roundname in df['RoundName'].unique()],
                placeholder="Select a Round",
                ),
                html.Br(),
                html.P(
                    "Match:", className="lead"
                ),
                dcc.Dropdown(
                id='match-dropdown',
                placeholder="Select a Match",
                )
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
    )
    return sidebar

## score graph
def update_score_graph(selected_match, selected_round, df):
    if selected_match is None or selected_round is None:
        return go.Figure()

    home_team, away_team = selected_match.split(' vs. ')
    match_data = df[(df['RoundName'] == selected_round) & (df['HomeTeamName'] == home_team) & (df['AwayTeamName'] == away_team)].copy()
    
    if match_data.empty:
        return go.Figure()

    score_home = match_data.iloc[0]['ScoreHome']
    score_away = match_data.iloc[0]['ScoreAway']

    ## figure 1 - scoreboard
    score_fig = go.Figure()

    # Add the title row
    score_fig.add_annotation(
        text=selected_round.capitalize(),
        xref="paper", yref="paper",
        x=0.5, y=0.95,
        showarrow=False,
        font=dict(size=48,
                  color='#002366'),
        align="center"
    )

    score_fig.add_annotation(
        text=f"<span style='color:darkslategrey; font-size: 36px;'>{home_team} <span style='color:darkblue; font-size: 36px;'>{score_home} : {score_away}</span> {away_team}</span>",
        xref="paper", yref="paper",
        x=0.5, y=0.25,
        showarrow=False,
        align="center",
        font=dict(size=48)
    )

    score_fig.update_layout(
        template='seaborn',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='#d2f6f6',
        paper_bgcolor='#d2f6f6',
        height=350,
    )

    return score_fig


## 2 team comp
def update_match_stats(selected_match, selected_round, df):
    # Ensure 'Value' column is numeric
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    
    if selected_match is None or selected_round is None:
        return go.Figure()

    home_team, away_team = selected_match.split(' vs. ')
    match_data = df[(df['RoundName'] == selected_round) & (df['HomeTeamName'] == home_team) & (df['AwayTeamName'] == away_team)].copy()
    
    if match_data.empty:
        return go.Figure()

    relevant_stats = ['Goals', 'Ball Possession', 'Total Attacks', 'Total Attempts', 'Goals scored', 'Big Chances']
    match_data = match_data[match_data['StatsName'].isin(relevant_stats)]
    
    home_data = match_data[match_data['TeamName'] == home_team]
    away_data = match_data[match_data['TeamName'] == away_team]

    # Determine the maximum value for the x-axes range
    max_value = max(home_data['Value'].max(), away_data['Value'].max())
    
    match_stats_fig = make_subplots(rows=1, 
                        cols=2, 
                        shared_yaxes=True,
                        horizontal_spacing=0,
                        specs=[[{}, {}]]
                        )

    match_stats_fig.add_trace(go.Bar(
        y=home_data['StatsName'],
        x=home_data['Value'],
        orientation='h',
        name=home_team,
        marker_color='#002366',
        text=home_data['Value'],
        textposition='outside',
        hovertemplate='<b>Strategy</b>: %{y}<br><b>Number</b>: %{x}<extra></extra>'
    ), row=1, col=1)

    match_stats_fig.add_trace(go.Bar(
        y=away_data['StatsName'],
        x=away_data['Value'],
        orientation='h',
        name=away_team,
        marker_color='#c9ddff',
        text=away_data['Value'],
        textposition='outside',
        hovertemplate='<b>Strategy</b>: %{y}<br><b>Number</b>: %{x}<extra></extra>'
    ), row=1, col=2)

    match_stats_fig.update_yaxes(dict(autorange="reversed"),)
    match_stats_fig.update_xaxes(showticklabels=False,title_text=f"{home_team}", range=[max_value * 1.5, 0], row=1, col=1)
    match_stats_fig.update_xaxes(showticklabels=False,title_text=f"{away_team}", range=[0, max_value * 1.5], row=1, col=2)
    match_stats_fig.update_layout(title_text=f"{home_team} vs {away_team} - {selected_round.capitalize()}",
	                  height=425,
                      title_x=0.5,
	                  xaxis1=dict(title=home_team),
                      xaxis2=dict(title=away_team),
                      showlegend=False,
                      margin=dict(l=80, r=80, t=40, b=80),
                      plot_bgcolor='#d2f6f6',
                      paper_bgcolor='#d2f6f6',
                     )
    return match_stats_fig