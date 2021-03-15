from datetime import datetime

import requests
from sunpy import time

_MISSION_BEGIN = time.parse_time(datetime(2020, 2, 1))
_NOW = time.parse_time(datetime.now())


def intervals(descriptor, level=None, low_latency=False):
    """
    Return the intervals of all data files available in the Solar Oribter
    Archive for a given data descriptor.

    Parameters
    ----------
    descriptor: str
        Data product descriptor. These can be found by searching for data on
        http://soar.esac.esa.int/soar/#search, and identifying the descriptor
        from the "Descriptor" column.
    level: int, optional
        If specified, restrict the results to a specific data processing level.
    low_latency: bool, optional
        If `True`, query low latency data instead of science data.

    Returns
    -------
    list[sunpy.time.TimeRange]
    """
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
    if low_latency:
        query['FROM'] = 'v_ll_data_item'
    else:
        query['FROM'] = 'v_sc_data_item'
    query['WHERE'] = (f"descriptor='{descriptor}'+AND+"
                      f"begin_time<='{end_time}'+AND+"
                      f"end_time>='{begin_time}'")
    if level is not None:
        query['WHERE'] += f"+AND+level='{level}'"
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
        intervals.append(time.TimeRange(start, end))

    # TODO: log the number of intervals found here
    return intervals
