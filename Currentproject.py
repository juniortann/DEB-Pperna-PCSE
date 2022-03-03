import numpy as np
import xarray as xr
import matplotlib.pylab as plt
import DEB_functions as DEB
import NCtools as nc
import pickle
# model the curve from CR experiments to control f!!!
# Geographical correlation ?
# talk about density dendence of feeding in the text
# Re-estimate parameters using literature data?
# EBmin??
# Use mean PIC from Ubatuba region to calibrate Y_K
# Include Lat and Lon in dict for nc NC_Data

# True PIC (SP3_max = 0.002) values don't really matter for the purpose of this simulation,
# what is important is that is varies accordingly to this calibration. It has a tiny variance.
with open('NC_LatLon.pickle', 'rb') as f:
    latlon = pickle.load(f)
lat = latlon['lat']
lon = latlon['lon']

SC1 = [-27.483333, -48.543333]

iSC1 = nc.locpixel(SC1, lat, lon)


L_i_corr[iSC1[0], (iSC1[1]-1)]
r_B_mean_corr[iSC1[0], (iSC1[1]-1)]
