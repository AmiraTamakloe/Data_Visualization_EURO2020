import pandas as pd

def drop_useless_columns(df):
    '''
        Drops the columns 'Event' and 'Time' from the dataframe and duplicates
        args:
            my_df: The dataframe to preprocess
        returns:
            The dataframe with rounded numbers
    '''
    df.drop(['Event', 'Time'], axis=1, inplace=True)
    df_games = df.drop_duplicates()
    df_games.to_csv('games_info.csv', index=False) 
    return df_games.round(2)

def get_statistics(df):
    '''
        compute statistics for the given dataframe
        args:
            df: The dataframe to compute statistics on
        returns:
            An array containing the total goal scored and conceded by each country with the goal difference
    '''
    country_stats = {}

    for _, row in df.iterrows():
        home_team = row['HomeTeamName']
        away_team = row['AwayTeamName']
        home_goals = row['ScoreHome']
        away_goals = row['ScoreAway']
        
        if home_team not in country_stats:
            country_stats[home_team] = {'Goal_Scored': 0, 'Goal_Conceded': 0}
        country_stats[home_team]['Goal_Scored'] += home_goals
        country_stats[home_team]['Goal_Conceded'] += away_goals
        
        if away_team not in country_stats:
            country_stats[away_team] = {'Goal_Scored': 0, 'Goal_Conceded': 0}
        country_stats[away_team]['Goal_Scored'] += away_goals
        country_stats[away_team]['Goal_Conceded'] += home_goals

    result_df = pd.DataFrame.from_dict(country_stats, orient='index').reset_index()
    result_df.columns = ['Country', 'Goal_Scored', 'Goal_Conceded']

    result_df['Goal_Difference'] = result_df['Goal_Scored'] - result_df['Goal_Conceded']
    result_df = result_df.sort_values(by='Goal_Difference', ascending=True)
    return result_df

def get_goals(df):
    """
    Transforms the dataframe to have a single column for team names and goals.
    
    Args:
        df: The dataframe with match information.
        
    Returns:
        A dataframe with team names and goals, without duplicate entries.
    """
    # Melt the dataframe to have a single column for team names and goals
    df_home = df[['MatchNumber', 'HomeTeamName', 'ScoreHome', 'MatchID', 'DateandTimeCET', 'RoundName']].rename(columns={'HomeTeamName': 'Team', 'ScoreHome': 'Goals'})
    df_away = df[['MatchNumber', 'AwayTeamName', 'ScoreAway', 'MatchID', 'DateandTimeCET', 'RoundName']].rename(columns={'AwayTeamName': 'Team', 'ScoreAway': 'Goals'})
    df_goals = pd.concat([df_home, df_away])

    # Remove duplicate entries
    df_goals = df_goals.drop_duplicates(subset=['MatchNumber', 'Team'])
    return df_goals

def calculate_goals(df):
    """
    Calculates total and average goals for each team.
    
    Args:
        df: The dataframe with match information.
        
    Returns:
        A dataframe with total and average goals for each team.
    """
    # Get the goals data
    df_goals = get_goals(df)

    # Group by team and calculate total and average goals
    df_goals_agg = df_goals.groupby('Team').agg(TotalGoals=('Goals', 'sum'), AvgGoals=('Goals', 'mean')).reset_index()
    return df_goals_agg


def vis5_get_total_goals(df_match_info):
    # convert 'DateandTimeCET' to datetime
    df_match_info['DateandTimeCET'] = pd.to_datetime(df_match_info['DateandTimeCET'])

    # group by MatchID and calculate total goals for each match
    df_match_info['TotalGoals'] = df_match_info['ScoreHome'] + df_match_info['ScoreAway']
    total_goals = df_match_info.groupby(['MatchID', 'HomeTeamName', 'AwayTeamName']).agg({'TotalGoals':'max'}).reset_index()

    # sort by total goals in descending order
    sorted_goals = total_goals.sort_values(by='TotalGoals', ascending=False)
    return sorted_goals

def vis7_get_outcome_percentage(df):
    # calculating match outcome
    df['Outcome'] = df.apply(lambda row: 'Win' if row['ScoreHome'] > row['ScoreAway'] else ('Draw' if row['ScoreHome'] == row['ScoreAway'] else 'Loss'), axis=1)
    # transforming the outcome into percentage
    outcome_percentage = df['Outcome'].value_counts(normalize=True) * 100
    return outcome_percentage
