import plotly.express as px

def init_figure():
    """
    Initializes an empty bar chart figure.

    Returns:
        fig (Figure): An empty Plotly bar chart figure.
    """
    fig = px.bar()
    return fig

def draw(fig, df_goals_agg):
    """
    Draws the bar chart based on the aggregated goals data frame.

    Args:
        fig (Figure): The initial empty figure to draw on.
        df_goals_agg (DataFrame): The data frame containing aggregated goals data.

    Returns:
        fig (Figure): The updated Plotly bar chart figure.
    """
    fig = px.bar(df_goals_agg, x='Team', y='TotalGoals', color='TotalGoals',
                 color_continuous_scale='Blues', title='Team Performance Bar Chart')
    return fig

def update_figure(df_goals_agg, selected_metric):
    """
    Updates the bar chart based on the selected metric (Total Goals or Average Goals).

    Args:
        df_goals_agg (DataFrame): The data frame containing aggregated goals data.
        selected_metric (str): The selected metric to display ('TotalGoals' or 'AvgGoals').

    Returns:
        fig (Figure): The updated Plotly bar chart figure.
    """
    fig = px.bar(df_goals_agg, x='Team', y=selected_metric, color=selected_metric,
                 color_continuous_scale='Blues', title='Team Performance Bar Chart')
    fig.update_traces(
        hovertemplate='<b>Team: %{x}</b><br>' +
                      ('AvgGoals: %{y:.2f}' if selected_metric == 'AvgGoals' else 'TotalGoals: %{y}')
    )
    return fig
