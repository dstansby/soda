from soda import soda
from soda import plot
from bokeh.io import show

intervals = soda.intervals('SWA-PAS-GRND-MOM')
p = plot.plot_intervals(intervals)
show(p)
