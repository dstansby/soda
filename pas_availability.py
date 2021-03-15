from soda import soda
from soda import plot
from bokeh.io import show

descriptors = ['SWA-PAS-GRND-MOM', 'MAG-RTN-NORMAL']
intervals = {desc: soda.intervals(desc) for desc in descriptors}
p = plot.plot_intervals(intervals)
show(p)
