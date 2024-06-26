5# -*- coding: utf-8 -*-
"""PrepProcess.ipynb

"""

import pandas as pd

def dataProcessing(DF_Data: pd.DataFrame) -> pd.DataFrame:
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

def calculateWinsLosses(final_results: pd.DataFrame) -> pd.DataFrame:
    # Initialize dictionaries to store wins and losses
    wins = {}
    losses = {}

    # Calculate wins and losses
    for index, row in final_results.iterrows():
        if row['ScoreHome'] > row['ScoreAway']:
            wins[row['HomeTeamName']] = wins.get(row['HomeTeamName'], 0) + 1
            losses[row['AwayTeamName']] = losses.get(row['AwayTeamName'], 0) + 1
        elif row['ScoreHome'] < row['ScoreAway']:
            wins[row['AwayTeamName']] = wins.get(row['AwayTeamName'], 0) + 1
            losses[row['HomeTeamName']] = losses.get(row['HomeTeamName'], 0) + 1
        else:
            # Draws are not counted in win-loss records
            continue

    # Convert to DataFrame for easier plotting
    win_loss_record = pd.DataFrame({'Wins': wins, 'Losses': losses}).fillna(0).astype(int)

    # Calculate the difference between wins and losses
    win_loss_record['Difference'] = win_loss_record['Wins'] - win_loss_record['Losses']

    # Sort by the difference
    #win_loss_record = win_loss_record.sort_values(by='Difference', ascending=False)
    win_loss_record = win_loss_record.sort_values(by=['Difference', 'Wins'], ascending=[False, False])
    return win_loss_record
