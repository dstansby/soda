from datetime import timedelta

from bokeh.io import show
from bokeh.models import MultiChoice
from bokeh.plotting import figure
from bokeh.layouts import layout, Spacer

from soda.availability import DataProduct


class DataAvailabilityPlotter:
    def __init__(self):
        self.plotter = figure(sizing_mode='stretch_width', plot_height=400,
                              title="Solar Orbiter data availability",
                              x_axis_type='datetime', y_range=[])
        self.plotter.ygrid.grid_line_color = None
        self.plotter.xaxis.axis_label = "Date"
        self.plotter.outline_line_color = None

        self.all_options = ['SWA-PAS-GRND-MOM', 'MAG-RTN-NORMAL',
                            'EUI-FSI304-IMAGE', 'EUI-FSI174-IMAGE']
        self.multi_choice = MultiChoice(
            value=['SWA-PAS-GRND-MOM', 'MAG-RTN-NORMAL'],
            options=self.all_options,
            width_policy='fit',
            width=300)

        self.layout = layout([[self.plotter],
                              [Spacer(), self.multi_choice, Spacer()]],
                             sizing_mode='stretch_width')

        # Add data
        for desc in self.all_options:
            self.add_interval_data(desc)

        self.multi_choice.js_link("value", self.plotter.y_range, "factors")
        self.plotter.y_range.factors = self.multi_choice.value

    def add_interval_data(self, descriptor):
        product = DataProduct(descriptor)
        dates_plotted = []
        for _, row in product.intervals.iterrows():
            date = row['Start'].date()
            if date not in dates_plotted:
                self.plotter.hbar(y=[descriptor],
                                  left=date,
                                  right=date + timedelta(days=1),
                                  height=0.5)
                dates_plotted.append(date)

    def show(self):
        show(self.layout)
