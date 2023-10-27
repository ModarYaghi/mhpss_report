import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

# Sample data
data = {'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Frequency': [1, 3, 2]}
df = pd.DataFrame(data)

# Plot
fig = go.Figure(data=go.Scatter(x=df['Date'], y=df['Frequency'], mode='lines'))
fig.update_layout(
    title='Frequency Plot',
    xaxis_title='Date',
    yaxis_title='Frequency',
    xaxis=dict(
        showline=True,
        linewidth=2,
        linecolor='black',
    ),
    yaxis=dict(
        showline=True,
        linewidth=2,
        linecolor='black',
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='black'),
)

# Show plot
plot(fig, filename='plot.html')

#%%
