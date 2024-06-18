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

# Read in match_info dataframe for pie chart
df_match = pd.read_excel('EURO_2020_DATA.xlsx', sheet_name = 'Match information')


# create a side bar for first column
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
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
        dbc.Col(dcc.Graph(id='score-graph'), width=9, align='center', style = {'margin-top':'3px'})
    ]),
    dbc.Row([
        dbc.Col(),
        dbc.Col(dcc.Graph(id='match_stats'),width=9, align='center', style={'margin-top': '3px'})
    ]),
    dbc.Row([
        dbc.Col(),
        dbc.Col(dcc.Graph(id='pie_chart'), width=9, style={'margin-top': '3px'})
    ]),
    dbc.Row([
        dbc.Col(),
        dbc.Col(dcc.Graph(id='num_goals'), width=9, style={'margin-top': '3px'})
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
    match_data = df[(df['RoundName'] == selected_round) & (df['HomeTeamName'] == home_team) & (df['AwayTeamName'] == away_team)].copy()
    
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
        # width=800, 
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
                    #   width=800, 
	                  height=425,
                      title_x=0.5,
	                  xaxis1=dict(title=home_team),
                      xaxis2=dict(title=away_team),
                      showlegend=False,
                      margin=dict(l=80, r=80, t=40, b=80)
                     )
    return match_stats_fig


## match_stats_fig
## figure 3 - win/loss pie chart
# Callback to update pie chart based on selected match
@app.callback(
    Output('pie_chart', 'figure'),
    Input('match-dropdown', 'value'),
    Input('roundname-dropdown', 'value')
)


def update_pie_chart(selected_match, selected_round):
    if selected_match is None or selected_round is None:
        return go.Figure()

    home_team, away_team = selected_match.split(' vs. ')
    match_home = df_match[(df_match['HomeTeamName'] == home_team)].copy()
    
    match_info = df_match.copy()
    
    if match_home.empty:
        return go.Figure()
    
    match_home['Outcome'] = match_home.apply(lambda row: 'Win' if row['ScoreHome'] > row['ScoreAway'] else ('Draw' if row['ScoreHome'] == row['ScoreAway'] else 'Loss'), axis=1)
    # All the matches outcome for Home team
    match_info['Outcome'] = df_match.apply(lambda row: 'Win' if row['ScoreHome'] > row['ScoreAway'] else ('Draw' if row['ScoreHome'] == row['ScoreAway'] else 'Loss'), axis=1)

    
    # Transforming the outcome into percentage
    outcome_percentage_home = match_home['Outcome'].value_counts(normalize=True) * 100

    outcome_percentage = match_info['Outcome'].value_counts(normalize=True) * 100
    
    # Create subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

    # Add the first pie chart
    fig.add_trace(go.Pie(labels=outcome_percentage_home.index, values=outcome_percentage_home, name=f"{home_team}", hole=.5), 1, 1)

    # Add the second pie chart
    fig.add_trace(go.Pie(labels=outcome_percentage.index, values=outcome_percentage, name="EURO 2020 Matches Outcome for Home Team", hole=.5), 1, 2)

    # Update layout
    fig.update_layout(
        title_text=f"Win/Loss/Draw Distribution for {home_team} and All Home Teams",
        title_x=0.5,
        annotations=[dict(text=f'{home_team}', x=0.225, y=0.5, font_size=18, showarrow=False, xanchor='center', yanchor='middle'),
                    dict(text='ALL', x=0.775, y=0.5, font_size=20, showarrow=False, xanchor='center', yanchor='middle')]
    )

    # pie_chart = go.Figure(data=[go.Pie(labels=outcome_percentage_home.index, values=outcome_percentage_home, hole=.35)])
    # pie_chart.update_layout(
    #     title_text=f"Win/Loss/Draw Distribution of EURO 2020 Matches Outcome for {home_team}",
    #     width=800,
    #     height=400,
    #     title_x=0.5,
    # )
    
    # return pie_chart
    return fig

## match_stats_fig
## figure 3 - win/loss pie chart
# Callback to update pie chart based on selected match
@app.callback(
    Output('num_goals', 'figure'),
    Input('match-dropdown', 'value'),
    Input('roundname-dropdown', 'value')
)

def update_num_goals(selected_match, selected_round):
    if selected_match is None or selected_round is None:
        return go.Figure()

    # For selected Round
    home_team, away_team = selected_match.split(' vs. ')
    match_data = df[(df['RoundName'] == selected_round) & (df['HomeTeamName'] == home_team) & (df['AwayTeamName'] == away_team)].copy()

    if match_data.empty:
        return go.Figure()

    match_data['TotalGoals'] = match_data['ScoreHome'] + match_data['ScoreAway']
    match_data['Match'] = match_data.apply(lambda row: f"{row['HomeTeamName']} vs {row['AwayTeamName']}", axis=1)

    # For total Gaming results
    total_goals = df_match.copy()
    total_goals['TotalGoals'] = total_goals['ScoreHome'] + total_goals['ScoreAway']
    total_goals['Match'] = total_goals.apply(lambda row: f"{row['HomeTeamName']} vs {row['AwayTeamName']}", axis=1)

    # Sort by total goals in descending order
    sorted_goals = total_goals.sort_values(by='TotalGoals', ascending=False)

    # Filter top 10 matches by total goals
    top_matches = sorted_goals.head(10)
    
    # Check if the selected match is in the top 10 matches
    selected_match_str = match_data['Match'].values[0]
    if selected_match_str in top_matches['Match'].values:
        # If the selected match is in the top 10, highlight it in red
        fig = px.bar(top_matches, 
                     x='TotalGoals', 
                     y='Match', 
                     orientation='h', 
                     title='Top EURO 2020 Matches by Total Goals Scored',
                     labels={'TotalGoals': 'Total Goals', 'y': 'Match'},
                     height=600)
        fig.update_layout(
                    title=dict(text='Top EURO 2020 Matches by Total Goals Scored', x=0.5),
                    xaxis_title='Total Goals',
                    yaxis_title='Match',
                    margin=dict(t=50) # Adjust top margin to make room for the title
                    )
        fig.update_traces(marker_color=top_matches['Match'].apply(lambda x: 'red' if x == selected_match_str else 'blue'))
    else:
        # If the selected match is not in the top 10, add it to the top and re-sort
        combined_matches = pd.concat([match_data[['Match', 'TotalGoals']], top_matches])
        combined_matches = combined_matches.drop_duplicates().sort_values(by='TotalGoals', ascending=False).head(11)

        # Create the bar chart
        fig = px.bar(combined_matches, 
                     x='TotalGoals', 
                     y='Match', 
                     orientation='h', 
                     title='Top EURO 2020 Matches by Total Goals Scored',
                     labels={'TotalGoals': 'Total Goals', 'y': 'Match'},
                     height=600)
        fig.update_layout(
                    title=dict(text='Top EURO 2020 Matches by Total Goals Scored', x=0.5),
                    xaxis_title='Total Goals',
                    yaxis_title='Match',
                    margin=dict(t=50) # Adjust top margin to make room for the title
                    )
        
        # Highlight the selected match in red and others in blue
        fig.update_traces(marker_color=combined_matches['Match'].apply(lambda x: 'red' if x == selected_match_str else 'blue'))

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)