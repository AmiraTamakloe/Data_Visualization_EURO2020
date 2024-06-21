import pandas as pd

def drop_useless_columns(df):
    """
    Drops unnecessary columns from the dataframe.
    
    Args:
        df: The original dataframe.
        
    Returns:
        A dataframe without the 'Event' and 'Time' columns.
    """
    # Drop the 'Event' and 'Time' columns
    df_filtered = df.drop(columns=['Event', 'Time'])
    return df_filtered

def get_statistics(df):
    """
    Extracts and processes match information from the dataframe.
    
    Args:
        df: The filtered dataframe.
        
    Returns:
        A dataframe with relevant match information and an added 'MatchNumber' column.
    """
    # Select relevant columns and create a 'MatchNumber' column
    df_matches_info = df[['HomeTeamName', 'AwayTeamName', 'DateandTimeCET', 'MatchID', 'RoundName', 'ScoreHome', 'ScoreAway']]
    df_matches_info['MatchNumber'] = df_matches_info.groupby('MatchID').ngroup() + 1
    return df_matches_info

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
