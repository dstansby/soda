import heliopy.data.spice as spicedata
import heliopy.spice as spice
from datetime import datetime, timedelta
import astropy.units as u
import numpy as np


spicedata.get_kernel('solo')
orbiter = spice.Trajectory('Solar Orbiter')
earth = spice.Trajectory('Earth')


def get_traj():
    starttime = datetime(2020, 2, 11)
    endtime = datetime.now() + timedelta(days=365)
    times = []
    while starttime < endtime:
        times.append(starttime)
        starttime += timedelta(days=1)

    orbiter.generate_positions(times, 'Sun', 'HEE')
    earth.generate_positions(times, 'Sun', 'HEE')
    adotb = ((orbiter.x.to_value(u.AU) * earth.x.to_value(u.AU) +
              orbiter.y.to_value(u.AU) * earth.y.to_value(u.AU) +
              orbiter.z.to_value(u.AU) * earth.z.to_value(u.AU)) /
             (orbiter.r.to_value(u.AU) * earth.r.to_value(u.AU)))
    sun_earth_angle = np.rad2deg(np.arccos(adotb))
    return times, orbiter.r.to_value(u.au), sun_earth_angle
