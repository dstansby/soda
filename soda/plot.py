from bokeh.plotting import figure
from datetime import timedelta

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
    for key, df in intervals.items():
        dates_plotted = []
        for _, row in intervals[key].iterrows():
            date = row['Start'].date()
            if date not in dates_plotted:
                p.hbar(y=[key],
                       left=date,
                       right=date + timedelta(days=1),
                       height=0.5)
                dates_plotted.append(date)

    p.ygrid.grid_line_color = None
    p.xaxis.axis_label = "Date"
    p.outline_line_color = None

    return p
