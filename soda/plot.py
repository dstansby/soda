from datetime import datetime, timedelta
import portion

from bokeh.io import output_file, show
from bokeh.models import MultiChoice, PanTool, BoxZoomTool, FixedTicker
from bokeh.plotting import figure
from bokeh.layouts import gridplot, Spacer

from soda.availability import DataProduct
from soda.trajectory import get_traj


class DataAvailabilityPlotter:
    def __init__(self, output_filename='soda.html'):
        output_file(output_filename, title='SODA')
        datestr = datetime.now().strftime('%Y-%m-%d')
        self.plotter = figure(sizing_mode='stretch_width', plot_height=400,
                              title=f"Solar Orbiter data availability (last updated {datestr}, daily resolution, all data available at http://soar.esac.esa.int/soar/)",
                              x_axis_type='datetime', y_range=[],
                              x_range=(datetime(2020, 2, 10), datetime.now()),
                              tools=[PanTool(dimensions='width'),
                                     BoxZoomTool(dimensions='width'),
                                     'undo',
                                     'redo',
                                     'reset',
                                     'save'])
        self.plotter.ygrid.grid_line_color = None
        self.plotter.xaxis.axis_label = "Date"
        self.plotter.outline_line_color = None

        self.all_options = ['SWA-PAS-GRND-MOM', 'SWA-EAS-PAD-PSD',
                            'MAG-RTN-NORMAL',
                            'EUI-FSI304-IMAGE', 'EUI-FSI174-IMAGE',
                            'EUI-HRILYA1216-IMAGE', 'EUI-HRIEUV174-IMAGE',
                            'RPW-BIA-DENSITY',
                            'EPD-EPT-ASUN-RATES', 'EPD-EPT-SUN-RATES',
                            'EPD-STEP-RATES',
                            ]

        self.all_options = sorted(self.all_options)
        self.multi_choice = MultiChoice(
            value=self.all_options,
            options=self.all_options,
            width_policy='fit',
            width=200,
            sizing_mode='stretch_height',
            title='Select data products')

        self.r_plot = figure(sizing_mode='stretch_width', plot_height=150,
                             x_axis_type='datetime', y_range=[0.3, 1],
                             x_range=self.plotter.x_range,
                             tools=[],
                             title='Radial distance')
        self.phi_plot = figure(sizing_mode='stretch_width', plot_height=150,
                               x_axis_type='datetime', y_range=[0, 180],
                               x_range=self.plotter.x_range,
                               tools=[],
                               title='Earth-Orbiter angle')
        self.phi_plot.yaxis[0].ticker = FixedTicker(ticks=[0, 90, 180])
        self.add_trajectory()

        self.layout = gridplot([[self.multi_choice, self.plotter],
                                [None, self.r_plot],
                                [None, self.phi_plot],
                                [None, Spacer()]],
                               sizing_mode='stretch_width')

        # Add data
        for desc in self.all_options:
            self.add_interval_data(desc)

        self.multi_choice.js_link("value", self.plotter.y_range, "factors")
        self.plotter.y_range.factors = self.multi_choice.value

    def add_interval_data(self, descriptor):
        product = DataProduct(descriptor)
        intervals = self.merge_intervals(product.intervals)
        for interval in intervals:
            self.plotter.hbar(y=[descriptor],
                              left=interval.lower,
                              right=interval.upper,
                              height=0.5,
                              color=self.get_color(descriptor))

    def add_trajectory(self):
        dates, r, sun_earth_angle = get_traj()
        self.r_plot.line(x=dates, y=r)
        self.phi_plot.line(x=dates, y=sun_earth_angle)

    @staticmethod
    def get_color(descriptor):
        return {'EUI': '#e41a1c',
                'MAG': '#377eb8',
                'SWA': '#4daf4a',
                'RPW': '#984ea3',
                'EPD': '#ff7f00'}[descriptor[:3]]

    @staticmethod
    def merge_intervals(intervals):
        intervals = intervals.sort_values(by='Start')
        start_dates = intervals['Start'].map(lambda t: t.date()).unique()
        end_dates = (intervals['End'] +
                     timedelta(days=1) -
                     timedelta(microseconds=1)).map(lambda t: t.date()).unique()
        intervals = portion.empty()
        for start, end in zip(start_dates, end_dates):
            intervals = intervals | portion.closed(start, end)
        return intervals

    def show(self):
        show(self.layout)
