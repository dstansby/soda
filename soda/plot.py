from bokeh.plotting import figure


def plot_intervals(intervals):
    """
    Parameters
    ----------
    intervals: dict[str: sunpy.time.TimeRange]

    Returns
    -------
    plotly.figure
    """
    ys = list(intervals.keys())
    p = figure(plot_width=800, plot_height=400,
               title="Solar Orbiter data availability", y_range=ys,
               x_axis_type='datetime')
    for key in intervals:
        for interval in intervals[key]:
            p.hbar(y=[key],
                   left=interval.start.datetime,
                   right=interval.end.datetime,
                   height=0.5)

    p.ygrid.grid_line_color = None
    p.xaxis.axis_label = "Date"
    p.outline_line_color = None

    return p
