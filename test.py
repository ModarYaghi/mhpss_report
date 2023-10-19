import plotly.graph_objects as go
import plotly.io as pio

# Global variables for easy editing
PLOT_TYPE = 'scatter'
TITLE = 'My Plot'
COLORS = 'red'
FONT_SIZE = 18
BG_OPACITY = 0.1
FILENAME = 'plot.png'

pio.renderers.default = 'browser'

def plot_data(*args, plot_type=PLOT_TYPE, title=TITLE, colors=COLORS, font_size=FONT_SIZE, bg_opacity=BG_OPACITY, **kwargs):
    fig = go.Figure()

    if plot_type == 'scatter':
        x, y = args
        fig.add_trace(go.Scatter(x=x, y=y, mode='markers', marker=dict(color=colors), **kwargs))
    elif plot_type == 'line':
        x, y = args
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color=colors), **kwargs))
    elif plot_type == 'bar':
        x, y = args
        fig.add_trace(go.Bar(x=x, y=y, marker=dict(color=colors), **kwargs))
    elif plot_type == 'pie':
        labels, values = args
        fig.add_trace(go.Pie(labels=labels, values=values, **kwargs))

    fig.update_layout(
        title=title,
        title_font=dict(size=font_size, color=colors),
        plot_bgcolor=f'rgba(0,0,0,{bg_opacity})' if bg_opacity is not None else None,
    )

    fig.update_traces(
        textfont=dict(size=font_size),
    )

    return fig


def save_plot(fig, filename=FILENAME):
    pio.write_image(fig, filename)


# Save scatter plot to image file
save_plot(scatter_plot)

labels = ['Female', 'Male']
values = [72, 79]

chart = plot_data(labels, values, plot_type='pie', title='Gender Distribution')
chart.show()

