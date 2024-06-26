import pandas as pd
import plotly.graph_objects as go


def show_heatmap(heatmap_data):

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Spectral',
        hovertemplate='Number of occurrences: %{z}<extra></extra>',
        colorbar=dict(title='Number of events')
    ))

    fig.update_layout(
        title='Event occurrences per time interval',
        xaxis_title='Time Interval (minutes)',
        yaxis_title='Event',
        autosize=False,
        height=700,
        width=1000,
        xaxis=dict(showline=False, showgrid=False),
        yaxis=dict(showline=False, showgrid=False),
        plot_bgcolor='#d2f6f6',
        paper_bgcolor='#d2f6f6',
    )

    return fig