from bokeh.plotting import figure


def plot_intervals(intervals):
    """
    Parameters
    ----------
    intervals: list[sunpy.time.TimeRange]

    Returns
    -------
    plotly.figure
    """
    ys = ['Data product']
    p = figure(plot_width=800, plot_height=400,
               title="Intervals", y_range=ys)
    for interval in intervals:
        p.hbar(y=ys, left=interval.start.datetime, right=interval.end.datetime,
               height=0.5)

    p.ygrid.grid_line_color = None
    p.xaxis.axis_label = "Time (seconds)"
    p.outline_line_color = None

    return p
