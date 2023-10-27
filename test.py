import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.io as pio

# class PlotTemplate:
#     def __init__(self, plot_type='scatter', title='My Plot', title_color='black',
#                  font_size=18, bg_color='white', bg_opacity=0.1, filename='plot.png',
#                  legend_size=12):
#         self.plot_type = plot_type
#         self.title = title
#         self.title_color = title_color
#         self.font_size = font_size
#         self.bg_color = bg_color
#         self.bg_opacity = bg_opacity
#         self.filename = filename
#         self.legend_size = legend_size
#
#     def plot_data(self, *args, **kwargs):
#         fig = go.Figure()
#
#         if self.plot_type == 'scatter':
#             x, y = args
#             fig.add_trace(go.Scatter(x=x, y=y, mode='markers', **kwargs))
#         elif self.plot_type == 'line':
#             x, y = args
#             fig.add_trace(go.Scatter(x=x, y=y, mode='lines', **kwargs))
#         elif self.plot_type == 'bar':
#             x, y = args
#             fig.add_trace(go.Bar(
#                 x=x,
#                 y=y,
#                 marker_color='skyblue',
#                 width=0.4,
#                 opacity=0.7,
#                 text=y,
#                 textposition='outside',
#             ))
#         elif self.plot_type == 'pie':
#             labels, values = args
#             fig.add_trace(go.Pie(labels=labels, values=values, **kwargs))
#
#         fig.update_layout(
#             title={
#                 'text': self.title,
#                 'x': 0.5,
#                 'xanchor': 'center',
#                 'font': dict(size=self.font_size, color=self.title_color),
#             },
#             plot_bgcolor=f'rgba({self.bg_color},{self.bg_opacity})',
#             legend=dict(font=dict(size=self.legend_size)),
#             xaxis_title='Age Group',
#             yaxis_title='Count',
#         )
#
#         fig.update_traces(
#             textfont=dict(size=self.font_size),
#         )
#
#         return fig
#
#     def set_bg_color(self, color, opacity):
#         self.bg_color = color
#         self.bg_opacity = opacity
#
#     def set_legend_size(self, size):
#         self.legend_size = size
#
#     def set_title(self, title, color, size):
#         self.title = title
#         self.title_color = color
#         self.font_size = size
#
#     def set_filename(self, filename):
#         self.filename = filename
#
#     # def save_plot(self, fig):
#     #     pio.write_image(fig, self.filename)


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


def format_quarter(date):
    q = (date.month - 1) // 3 + 1
    return f"{date.year}-Q{q}"


df = pd.read_csv('visits23.csv')
df['date'] = pd.to_datetime(df['date'])
df = df['date'].value_counts().reset_index()
df.columns = ['Date', 'Frequency']
df.sort_values('Date', inplace=True)

start_date = df['Date'].min().strftime('%Y-%m-%d')
end_date = df['Date'].max().strftime('%Y-%m-%d')
quarters = pd.date_range(start=start_date, end=end_date, freq='Q')
tickvals = [start_date] + [d.strftime('%Y-%m-%d') for d in quarters] + [end_date]
ticktext = [start_date] + [format_quarter(d) for d in quarters] + [end_date]

fig = go.Figure(data=go.Scatter(x=df['Date'].dt.strftime('%Y-%m-%d'), y=df['Frequency'], mode='lines'))
fig.update_layout(
    title='Visit Frequency Over Time',
    title_font=dict(size=24),
    xaxis_title='Date',
    yaxis_title='Frequency',
    xaxis=dict(
        range=[start_date, end_date],
        tickmode='array',
        tickvals=tickvals,
        ticktext=ticktext,
        showline=True,
        linewidth=2
    ),
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgrey'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='black')
)

plot(fig, filename='plot.html')
