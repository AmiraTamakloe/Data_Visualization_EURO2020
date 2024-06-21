import plotly.express as px
import preprocess

def draw(df):
    df_goals = preprocess.get_goals(df)
    heatmap_data = df_goals.pivot(index='Team', columns='MatchNumber', values='Goals').fillna(0)
    fig = px.imshow(heatmap_data,
                    labels=dict(x="Match Number", y="Teams", color="Total Goals"),
                    color_continuous_scale='Blues',
                    title='Total Goals per Team per Match')
    return fig

def update_figure(df, selected_metric):
    df_goals = preprocess.get_goals(df)
    if selected_metric == 'TotalGoals':
        heatmap_data = df_goals.pivot(index='Team', columns='MatchNumber', values='Goals').fillna(0)
        color_label = "Total Goals"
    else:
        matches_played = df_goals.groupby('Team')['MatchNumber'].nunique()
        heatmap_data = df_goals.pivot(index='Team', columns='MatchNumber', values='Goals').fillna(0).div(matches_played, axis=0)
        color_label = "AvgGoals"

    fig = px.imshow(heatmap_data,
                    labels=dict(x="Match Number", y="Teams", color=color_label),
                    color_continuous_scale='Blues',
                    title=f'{color_label} per Team per Match')

    customdata = []
    for match_number in heatmap_data.columns:
        match_info = df[df['MatchNumber'] == match_number].iloc[0]
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
                customdata_row.append("null")
        customdata_matrix.append(customdata_row)

    for trace in fig.data:
        trace.customdata = customdata_matrix
        trace.hovertemplate = (
            'Team: %{y}<br>' +
            'Match Number: %{x}<br>' +
            ('AvgGoals: %{z:.2f}<br>' if selected_metric == 'AvgGoals' else 'TotalGoals: %{z}<br>') +
            'Match: %{customdata}<extra></extra>'
        )

    fig.update_layout(
        autosize=False,
        height=600,
        margin=dict(l=0, r=0, t=30, b=30),
        xaxis=dict(showgrid=True, gridcolor='black', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='black', zeroline=False)
    )

    return fig

