from bokeh.plotting import figure

import astropy.units as u
from sunpy.time import TimeRange


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
        dates = filter_intervals(intervals[key])
        for interval in dates:
            p.hbar(y=[key],
                   left=interval.start.datetime,
                   right=interval.end.datetime,
                   height=0.5)

    p.ygrid.grid_line_color = None
    p.xaxis.axis_label = "Date"
    p.outline_line_color = None

    return p


def filter_intervals(intervals):
    out = []
    for interval in intervals:
        for date in interval.get_dates():
            if date not in out:
                out.append(date)
    out = sorted(out)
    return [TimeRange(t, t + 1*u.day) for t in out]
