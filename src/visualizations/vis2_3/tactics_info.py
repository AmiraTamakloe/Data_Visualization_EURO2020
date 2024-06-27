# callbacks.py
from visualizations.match_comp import match_comp
from dash.dependencies import Input, Output

def register_callbacks(app, df_comparison):
    
    @app.callback(
        Output('match-dropdown', 'options'),
        Input('roundname-dropdown', 'value')
    )
    def set_match_options(selected_round):
        if selected_round is None:
            return []

         # Capitalize the round name
        # selected_round = selected_round.capitalize() 
        filtered_df = df_comparison[df_comparison['RoundName'] == selected_round]
        matches = filtered_df[['HomeTeamName', 'AwayTeamName']].drop_duplicates()
        match_options = [{'label': f"{row['HomeTeamName']} vs. {row['AwayTeamName']}", 'value': f"{row['HomeTeamName']} vs. {row['AwayTeamName']}"} for _, row in matches.iterrows()]
        return match_options

    @app.callback(Output('score-graph', 'style'), [Input('match-dropdown', 'value'), Input('roundname-dropdown', 'value')])
    def hide_score_graph(input1, input2):
        if input1 is not None and input2 is not None:
            return {'display': 'block'}
        else:
            return {'display': 'none'}

    @app.callback(
        Output('score-graph', 'figure'),
        Input('match-dropdown', 'value'),
        Input('roundname-dropdown', 'value')
    )
    def update_score_graph(selected_match, selected_round):
        return match_comp.update_score_graph(selected_match, selected_round, df_comparison)

    @app.callback(Output('match_stats', 'style'), [Input('match-dropdown', 'value'), Input('roundname-dropdown', 'value')])
    def hide_match_stats_graph(input1, input2):
        if input1 is not None and input2 is not None:
            return {'display': 'block'}
        else:
            return {'display': 'none'}

    @app.callback(
        Output('match_stats', 'figure'),
        Input('match-dropdown', 'value'),
        Input('roundname-dropdown', 'value')
    )
    def update_match_stats(selected_match, selected_round):
        return match_comp.update_match_stats(selected_match, selected_round, df_comparison)
