import pickle
import numpy as np
import matplotlib.pyplot as plt


def locpixel(latlon, latstr, lonstr):
    """
    Locate the pixel index from coordinates
    Input:
     - latlon = list with [latitude, longitude] of interest
     - latstr = list of latitudes from data
     - lonstr = list of longitude from data
    """
    ploc_lat = np.append(latstr, latlon[0])
    ploc_lat.sort()  # ploc_lat = np.flip(ploc_lat)
    ploc_lon = np.append(lonstr, latlon[1])
    ploc_lon.sort()  # ploc_lon = np.flip(ploc_lon)
    # Had to correct Lat to get real values
    plat_i = np.array(len(latstr))-np.where(ploc_lat == latlon[0])
    plon_i = np.where(ploc_lon == latlon[1])

    return (int(plat_i[0]), int(plon_i[0]))


# Locate values geographically
with open('NC_LatLon.pickle', 'rb') as f:
    latlon = pickle.load(f)

with open('NC_Data.pickle', 'rb') as f:
    envdata = pickle.load(f)


# Ubatuba, Brazil

SP3 = (-23.429445, -45.053849)
lat = latlon['lat']
lon = latlon['lon']

iSP3 = locpixel(SP3, lat, lon)

var = 'POC'
POC_SP3 = []
for year in envdata[var].keys():
    POC_SP3.append(envdata[var][year][iSP3])

# SP3 POC info
POC_mean = np.mean(POC_SP3)
POC_median = np.median(POC_SP3)
POC_variance = np.var(POC_SP3)
POC_max = np.max(POC_SP3)
POC_min = np.min(POC_SP3)
print(POC_mean, POC_median, POC_variance, POC_max, POC_min)

plt.hist(POC_SP3)


# Let's see for Santos data
Santos = (-24.008396, -46.325536)  # Santos
iSantos = locpixel(Santos, lat, lon)

vars = list(envdata.keys())[0:3]
values = [envdata[var]['2006'][iSantos]
          for var in vars[0:3]]  # environmental variables from the pixel
for i in range(len(vars)):
    print('Santos: \n' + vars[i] + ': ' + str(values[i]))


# Armalção de Itapocoroy (Pennha, Brazil)

SC2 = (-26.771432, -48.607500)  # Armação de Itapocoroy

iSC2 = locpixel(SC2, lat, lon)

var = 'POC'
POC_SC2 = []
for year in envdata[var].keys():
    POC_SC2.append(envdata[var][year][iSC2])

POC_mean = np.mean(POC_SC2)
POC_median = np.median(POC_SC2)
POC_variance = np.var(POC_SC2)
POC_max = np.max(POC_SC2)
POC_min = np.min(POC_SC2)
print(POC_mean, POC_median, POC_variance, POC_max, POC_min)

plt.hist(POC_SC2)

envdata['POC']['2008'][locpixel((-27.495422, -48.539923), lat, lon)]
