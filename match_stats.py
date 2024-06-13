import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio


from plotly.subplots import make_subplots
import pandas as pd


# Ref: https://github.com/charlotteamy/Dash-visualisation/blob/main/Dash_blog.py
# Accroding to: https://www.coachesvoice.com/cv/italy-1-england-1-euro-2020-tactical-analysis/
# TO-DO: Try to create the same table!

# Read in 'project_data.csv'
df = pd.read_csv('data.csv')

# Ensure 'Value' column is numeric
df['Value'] = pd.to_numeric(df['Value'], errors='coerce')


# create a side bar for first column
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [
        html.H2("Match Statistics"),
        html.Hr(),
        html.P(
            "Gaming Results:", className="lead"
        ),
        dbc.Nav(
            [
                dcc.Dropdown(
                id='roundname-dropdown',
                options=[{'label': roundname, 'value': roundname} for roundname in df['RoundName'].unique()],
                placeholder="Select a Round",
                ),
                html.Br(),
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



# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[
    dbc.Row([
        dbc.Col(),
        dbc.Col(html.H1('A Visualization of Gaming Results'), width=9, style={'text-align': 'center', 'margin-top': '7px'})
    ]),
    dbc.Row([
        dbc.Col(sidebar),
        dbc.Col(dcc.Graph(id='score-graph'), width=9,style = {'margin-left': '26rem', 'margin-top':'3px'})
    ]),
    dbc.Row([
        dbc.Col(),
        dbc.Col(dcc.Graph(id='match_stats'),width=9, style={'margin-left': '26rem', 'margin-top': '3px'})
    ])
])
# Define the layout
# app.layout = html.Div(children=[
#     dbc.Row([
#         dbc.Col(html.H1('A Visualization of Gaming Results'), width=12, style={'text-align': 'center', 'margin-top': '7px'}),
#     ]),
#     dbc.Row([
#         dbc.Col(sidebar, width=3),
#         dbc.Col(
#             [
#                 dbc.Row([
#                     dbc.Col(dcc.Graph(id='score-graph')),
#                     dbc.Col(dcc.Graph(id='match_stats'))
#                 ]),
#             ],
#             width=9,
#         ),
#     ])
# ])

@app.callback(
    Output('match-dropdown', 'options'),
    Input('roundname-dropdown', 'value')
)
def set_match_options(selected_round):
    if selected_round is None:
        return []

    filtered_df = df[df['RoundName'] == selected_round]
    matches = filtered_df[['HomeTeamName', 'AwayTeamName']].drop_duplicates()
    match_options = [{'label': f"{row['HomeTeamName']} vs. {row['AwayTeamName']}", 'value': f"{row['HomeTeamName']} vs. {row['AwayTeamName']}"} for _, row in matches.iterrows()]
    return match_options

# create update figure for gaimng results
@app.callback(
    Output('score-graph', 'figure'),
    Input('match-dropdown', 'value'),
    Input('roundname-dropdown', 'value')
)

def update_score_graph(selected_match, selected_round):
    if selected_match is None or selected_round is None:
        return go.Figure()

    home_team, away_team = selected_match.split(' vs. ')
    match_data = df[(df['RoundName'] == selected_round) & (df['HomeTeamName'] == home_team) & (df['AwayTeamName'] == away_team)]
    
    if match_data.empty:
        return go.Figure()

    score_home = match_data.iloc[0]['ScoreHome']
    score_away = match_data.iloc[0]['ScoreAway']

    ## figure 1 - scoreboard
    score_fig = go.Figure()

    # Add the title row
    score_fig.add_annotation(
        text=selected_round,
        xref="paper", yref="paper",
        x=0.5, y=0.95,
        showarrow=False,
        font=dict(size=48,
                  color='#1f77b4'),
        # bgcolor="lightgreen",
        align="center"
    )

    score_fig.add_annotation(
        text=f"<span style='color:darkslategrey; font-size: 36px;'>{home_team} <span style='color:red; font-size: 36px;'>{score_home} : {score_away}</span> {away_team}</span>",
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
        width=800, 
	    height=350,
    )

    return score_fig

    
## match_stats_fig
## figure 2 - match bar chart
@app.callback(
    Output('match_stats', 'figure'),
    Input('match-dropdown', 'value'),
    Input('roundname-dropdown', 'value')
)

def update_match_stats(selected_match, selected_round):
    if selected_match is None or selected_round is None:
        return go.Figure()

    home_team, away_team = selected_match.split(' vs. ')
    match_data = df[(df['RoundName'] == selected_round) & (df['HomeTeamName'] == home_team) & (df['AwayTeamName'] == away_team)]
    
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
        marker_color='#4472c4',
        text=home_data['Value'],
        textposition='outside'
    ), row=1, col=1)

    match_stats_fig.add_trace(go.Bar(
        y=away_data['StatsName'],
        x=away_data['Value'],
        orientation='h',
        name=away_team,
        marker_color='#ed7d31',
        text=away_data['Value'],
        textposition='outside'
    ), row=1, col=2)

    match_stats_fig.update_yaxes(dict(autorange="reversed"),)
    match_stats_fig.update_xaxes(showticklabels=False,title_text=f"{home_team}", range=[max_value * 1.5, 0], row=1, col=1)
    match_stats_fig.update_xaxes(showticklabels=False,title_text=f"{away_team}", range=[0, max_value * 1.5], row=1, col=2)
    match_stats_fig.update_layout(title_text=f"{home_team} vs {away_team} - {selected_round}",
                      width=800, 
	                  height=400,
                      title_x=0.6,
	                  xaxis1=dict(title=home_team),
                      xaxis2=dict(title=away_team),
                      showlegend=False,
                      margin=dict(l=20, r=20, t=40, b=80)
                     )
    return match_stats_fig

if __name__ == '__main__':
    app.run_server(debug=True)