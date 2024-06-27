'''
    Contains some functions related to the creation of the bar chart.
    The bar chart displays the data either as counts or as percentages.
'''

import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.colors as mcolors


def init_figure():
    '''
        Initializes the Graph Object figure used to display the bar chart.
        Sets the template to be used to "simple_white" as a base with
        our custom template on top. Sets the title to 'Lines per act'

        Returns:
            fig: The figure which will display the bar chart
    '''
    fig = go.Figure()
    fig.update_layout(
        template=pio.templates['plotly_white'],
        dragmode=False,
        barmode='relative',
        title='Goal Difference by Country'
    )

    return fig


def draw(fig, data):
    '''
        Draws the bar chart.

        Args:
            fig: The figure comprising the bar chart
            data: The data to be displayed
        Returns:
            fig: The figure comprising the drawn bar chart
    '''

    fig = go.Figure(fig)
    countries = data['Country'].unique()

    blue_to_green = mcolors.LinearSegmentedColormap.from_list('blue_to_green', ['blue', 'green'])
    norm = mcolors.Normalize(vmin=data['Goal_Difference'].min(), vmax=data['Goal_Difference'].max())
    
    for country in countries:
        country_info = data[data['Country'] == country]
        x_values = [country]
        y_values = country_info['Goal_Difference']
        goals_scored = country_info['Goal_Scored'].values[0]
        goals_conceded = country_info['Goal_Conceded'].values[0]
        bar_color = mcolors.to_hex(blue_to_green(norm(y_values.values[0])))

        fig.add_trace(go.Bar(
            x=x_values,
            y=y_values,
            name=country,
            customdata=[(goals_scored, goals_conceded)],
            hovertemplate="<b>%{x}</b><br>Goal Difference: %{y}<br>Goals Scored: %{customdata[0]}<br>Goals Conceded: %{customdata[1]}<extra></extra>",
            marker_line_color='black',
            marker_line_width=1.5,
            marker=dict(
                color=bar_color,
                line=dict(color='black', width=1.5)
            )
        ))

    fig.update_layout(
        yaxis=dict(tickmode='linear', tick0=0, dtick=1),
        title={'text': "Goal Difference by Country", 'x': 0.5, 'xanchor': 'center'},
        xaxis_tickangle=-45,
        plot_bgcolor='#d2f6f6',
        paper_bgcolor='#d2f6f6',
    )
    return fig