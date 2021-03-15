from datetime import datetime, date
import pathlib
import pandas as pd

import requests
from sunpy import time

_MISSION_BEGIN = time.parse_time(datetime(2020, 1, 1))
_NOW = time.parse_time(datetime.now())
_CACHE_DIR = (pathlib.Path(__file__) / '..' / '.data').resolve()
_CACHE_DIR.mkdir(exist_ok=True)


class DataProduct:
    def __init__(self, descriptor, level=2, low_latency=False):
        """
        Parameters
        ----------
        descriptor: str
            Data product descriptor. These can be found by searching for data on
            http://soar.esac.esa.int/soar/#search, and identifying the descriptor
            from the "Descriptor" column.
        level: int, optional
            Data processing level. Defaults to 2.
        low_latency: bool, optional
            If `True`, query low latency data instead of science data.
        """
        self.descriptor = descriptor
        self.level = level
        self.low_latency = low_latency

    @property
    def latest_path(self):
        """
        Path to data updated today.
        """
        datestr = _NOW.strftime('%Y-%m-%d')
        return _CACHE_DIR / f'{self.descriptor}_L{self.level}_{datestr}.csv'

    @property
    def intervals(self):
        """
        All available intervals for this data product.
        """
        if not self.latest_path.exists():
            self.save_remote_intervals()

        df = pd.read_csv(self.latest_path,
                         parse_dates=['Start', 'End'])
        return df

    def save_remote_intervals(self):
        """
        Get and save the intervals of all data files available in the
        Solar Oribter Archive for a given data descriptor.
        """
        print(f'Updating intervals for {self.descriptor}...')
        base_url = ('http://soar.esac.esa.int/soar-sl-tap/tap/'
                    'sync?REQUEST=doQuery&')
        begin_time = _MISSION_BEGIN.isot.replace('T', '+')
        end_time = _NOW.isot.replace('T', '+')
        # Need to manually set the intervals based on a query
        request_dict = {}
        request_dict['LANG'] = 'ADQL'
        request_dict['FORMAT'] = 'json'

        query = {}
        query['SELECT'] = '*'
        if self.low_latency:
            query['FROM'] = 'v_ll_data_item'
        else:
            query['FROM'] = 'v_sc_data_item'
        query['WHERE'] = (f"descriptor='{self.descriptor}'+AND+"
                          f"begin_time<='{end_time}'+AND+"
                          f"begin_time>='{begin_time}'")
        # TODO: include error
        # if self.level is not None:
        #     query['WHERE'] += f"+AND+level='{self.level}'"
        request_dict['QUERY'] = '+'.join([f'{item}+{query[item]}' for
                                          item in query])

        request_str = ''
        request_str = [f'{item}={request_dict[item]}' for item in request_dict]
        request_str = '&'.join(request_str)

        url = base_url + request_str
        # Get request info
        r = requests.get(url)
        # TODO: intelligently detect and error on a bad descriptor

        # Do some list/dict wrangling
        names = [m['name'] for m in r.json()['metadata']]
        info = {name: [] for name in names}
        for entry in r.json()['data']:
            for i, name in enumerate(names):
                info[name].append(entry[i])

        # Setup intervals
        intervals = []
        for start, end in zip(info['begin_time'], info['end_time']):
            intervals.append([time.parse_time(start).datetime,
                              time.parse_time(end).datetime])

        df = pd.DataFrame(intervals)
        df.columns = ['Start', 'End']
        df.to_csv(self.latest_path, index=False)
