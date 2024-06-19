import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset from the CSV file
df = pd.read_csv('data.csv')


print(df.head())
print(df.columns)

# Extract relevant match information
df_matches_info = df[['HomeTeamName', 'AwayTeamName', 'DateandTimeCET', 'MatchID', 'RoundName', 'ScoreHome', 'ScoreAway', 'Event', 'Time']]

# Create a new column for the match number
df_matches_info['MatchNumber'] = df_matches_info.groupby('MatchID').ngroup() + 1

df_home = df_matches_info[['MatchNumber', 'HomeTeamName', 'ScoreHome', 'MatchID']].rename(columns={'HomeTeamName': 'Team', 'ScoreHome': 'Goals'})
df_away = df_matches_info[['MatchNumber', 'AwayTeamName', 'ScoreAway', 'MatchID']].rename(columns={'AwayTeamName': 'Team', 'ScoreAway': 'Goals'})
df_goals = pd.concat([df_home, df_away])

# Remove duplicate entries
df_goals = df_goals.drop_duplicates(subset=['MatchNumber', 'Team'])

# Calculate total and average goals for each team
df_goals_agg = df_goals.groupby('Team').agg(TotalGoals=('Goals', 'sum'), AvgGoals=('Goals', 'mean')).reset_index()


# Dash app
app = dash.Dash(__name__)

# layout of the app
app.layout = html.Div([
    dcc.Dropdown(
        id='metric-dropdown',
        options=[
            {'label': 'Total Goals', 'value': 'TotalGoals'},
            {'label': 'Average Goals', 'value': 'AvgGoals'}
        ],
        value='TotalGoals',
        style={'width': '50%'}
    ),
    dcc.Graph(id='performance-bar-chart'),
    dcc.Graph(id='team-goals-heatmap')
])

# Callback to update the bar chart and heatmap based on selected metric
@app.callback(
    [Output('performance-bar-chart', 'figure'),
     Output('team-goals-heatmap', 'figure')],
    [Input('metric-dropdown', 'value')]
)
def update_graphs(selected_metric):
    # Bar chart
    bar_chart_fig = px.bar(df_goals_agg, x='Team', y=selected_metric, color=selected_metric,
                           color_continuous_scale='Blues', title='Team Performance Bar Chart')
    
   
    bar_chart_fig.update_traces(
        hovertemplate='<b>Team: %{x}</b><br>' + 
                      ('AvgGoals: %{y:.2f}' if selected_metric == 'AvgGoals' else 'TotalGoals: %{y}')
    )

    # Heatmap for total goals or average goals
    if selected_metric == 'TotalGoals':
        heatmap_data = df_goals.pivot(index='Team', columns='MatchNumber', values='Goals').fillna(0)
        color_label = "Total Goals"
    else:
        heatmap_data = df_goals.pivot(index='Team', columns='MatchNumber', values='Goals').fillna(0) / df_goals['MatchNumber'].max()
        color_label = "AvgGoals"
    
    heatmap_fig = px.imshow(heatmap_data, 
                            labels=dict(x="Match Number", y="Teams", color=color_label),
                            color_continuous_scale='Blues',
                            title=f'{color_label} per Team per Match')

    #  extracts the home team and away team for each matc
    customdata = []
    for match_number in heatmap_data.columns:
        match_info = df_matches_info[df_matches_info['MatchNumber'] == match_number].iloc[0]
        customdata.append((match_info['HomeTeamName'], match_info['AwayTeamName']))

    
    customdata_matrix = []
    for team in heatmap_data.index:
        customdata_row = []
        for match_number in heatmap_data.columns:
            match = df_goals[(df_goals['Team'] == team) & (df_goals['MatchNumber'] == match_number)]
            if not match.empty:
                home_team, away_team = customdata[match_number - 1]  
                if team == home_team:
                    customdata_row.append(f"{home_team} vs {away_team}")
                else:
                    customdata_row.append(f"{away_team} vs {home_team}")
            else:
                customdata_row.append(None)
        customdata_matrix.append(customdata_row)

    for trace in heatmap_fig.data:
        trace.customdata = customdata_matrix
        trace.hovertemplate = (
            'Team: %{y}<br>' +
            'Match Number: %{x}<br>' +
            ('AvgGoals: %{z:.2f}<br>' if selected_metric == 'AvgGoals' else 'TotalGoals: %{z}<br>') +
            'Match: %{customdata}<extra></extra>'
        )

    heatmap_fig.update_layout(
        autosize=False,
        height=600,  # Adjust the height as needed
        margin=dict(l=0, r=0, t=30, b=30),
        xaxis=dict(showgrid=True, gridcolor='black', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='black', zeroline=False)
    )

    return bar_chart_fig, heatmap_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
