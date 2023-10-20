import plotly.graph_objects as go
import plotly.io as pio


class PlotTemplate:
    def __init__(self, plot_type='scatter', title='My Plot', title_color='black',
                 font_size=18, bg_color='white', bg_opacity=0.1, filename='plot.png',
                 legend_size=12):
        self.plot_type = plot_type
        self.title = title
        self.title_color = title_color
        self.font_size = font_size
        self.bg_color = bg_color
        self.bg_opacity = bg_opacity
        self.filename = filename
        self.legend_size = legend_size

    def plot_data(self, *args, **kwargs):
        fig = go.Figure()

        if self.plot_type == 'scatter':
            x, y = args
            fig.add_trace(go.Scatter(x=x, y=y, mode='markers', **kwargs))
        elif self.plot_type == 'line':
            x, y = args
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', **kwargs))
        elif self.plot_type == 'bar':
            x, y = args
            fig.add_trace(go.Bar(
                x=x,
                y=y,
                marker_color='skyblue',
                width=0.4,
                opacity=0.7,
                text=y,
                textposition='outside',
            ))
        elif self.plot_type == 'pie':
            labels, values = args
            fig.add_trace(go.Pie(labels=labels, values=values, **kwargs))

        fig.update_layout(
            title={
                'text': self.title,
                'x': 0.5,
                'xanchor': 'center',
                'font': dict(size=self.font_size, color=self.title_color),
            },
            plot_bgcolor=f'rgba({self.bg_color},{self.bg_opacity})',
            legend=dict(font=dict(size=self.legend_size)),
            xaxis_title='Age Group',
            yaxis_title='Count',
        )

        fig.update_traces(
            textfont=dict(size=self.font_size),
        )

        return fig

    def set_bg_color(self, color, opacity):
        self.bg_color = color
        self.bg_opacity = opacity

    def set_legend_size(self, size):
        self.legend_size = size

    def set_title(self, title, color, size):
        self.title = title
        self.title_color = color
        self.font_size = size

    def set_filename(self, filename):
        self.filename = filename

    # def save_plot(self, fig):
    #     pio.write_image(fig, self.filename)


if __name__ == "__main__":
    pass

# N = 154
#
# # Example usage
# template = PlotTemplate(
#     plot_type='pie',
#     title=f'Screening New Client Sex Distribution (N={N})',
#     title_color='black',
#     font_size=30,
#     bg_color='0,0,0',
#     bg_opacity=0.1,
#     filename='pie_chart.png'
# )
#
# template.set_bg_color('128,128,128', 0)
# template.set_legend_size(16)
# labels = ['Female', 'Male']
# values = [72, 79]
# chart = template.plot_data(labels, values)
# chart.show()
