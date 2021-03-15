from soda.availability import DataProduct
from soda import plot
from bokeh.io import show

descriptors = ['SWA-PAS-GRND-MOM', 'MAG-RTN-NORMAL',
               'EUI-FSI304-IMAGE', 'EUI-FSI174-IMAGE']
products = [DataProduct(desc) for desc in descriptors]
intervals = {prod.descriptor: prod.intervals for prod in products}
p = plot.plot_intervals(intervals)
show(p)
