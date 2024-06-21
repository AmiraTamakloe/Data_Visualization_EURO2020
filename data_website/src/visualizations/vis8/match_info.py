import pandas as pd
import plotly.graph_objects as go


def show_heatmap():
    data = pd.read_csv('matchaEventData.csv')

    bins = [0, 15, 30, 45, 60, 75, 90]
    labels = ['0-15', '15-30', '30-45', '45-60', '60-75', '75-90']
    data['TimeInterval'] = pd.cut(data['Minute'], bins=bins, labels=labels, right=False)

    heatmap_data = data.groupby(['Event', 'TimeInterval']).size().unstack(fill_value=0)

    heatmap_data = heatmap_data.loc[(heatmap_data != 0).any(axis=1)]

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Spectral',
        hovertemplate='Number of occurrences: %{z}<extra></extra>'
    ))

    fig.update_layout(
        title='Event occurrences per time interval',
        xaxis_title='Time Interval (minutes)',
        yaxis_title='Event',
        width=800,
        height=600,
        xaxis=dict(showline=False, showgrid=False),
        yaxis=dict(showline=False, showgrid=False)
    )

    return fig