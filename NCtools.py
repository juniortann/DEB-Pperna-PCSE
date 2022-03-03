from xarray import open_dataset
from os import listdir
import numpy as np
from collections import OrderedDict


def nc2dict(d):
    """
    Returns dictionary with nc variables and values in a directory
    containing a timeseries of nc files with the same variable
    Input:
    d = directory name within cwd
    Example:
    d = 'NC_CHL'
    nc2dict(d)
    """
    # Directory locations
    dir = d

    # Save filenames as strings
    dinfo = listdir(dir)
    files = [dir+'/'+dinfo for dinfo in dinfo] # Get files in directory
    files.sort()
    # Extract variable
    ds = open_dataset(files[0]) #change number for i
    var = list(ds.variables)[0]
    data = dict() # create empty dictionary to store the data
    data['lat'] = np.array(ds['lat'])
    data['lon'] = np.array(ds['lon'])

    # Reading data
    for file in files:
        ds_i = open_dataset(file) #change number for i
        var_i = list(ds_i.variables)[0]

        year_i = ds_i.attrs['time_coverage_start'][0:4]
        values_i = np.array(ds_i[var_i])
        data[year_i] = values_i

    return data

def nc_mergedicts(l):
    """
    Takes in a list with directory names and creates a
    dictionary with nc variables.
    Input: List with strings containing directory filenames
    Example:
    l = ['NC_CHL', 'NC_SST', 'NC_PIC']
    nc_mergedicts(l)
    """
    d = dict()
    for folder in l:
        d[folder[-3:]] = nc2dict(folder)

    return d

def locpixel(latlon, latstr, lonstr):
    """
    Locate the pixel index from coordinates
    Input:
     - latlon = list with [latitude, longitude] of interest
     - latstr = list of latitudes from data
     - lonstr = list of longitude from data
    """
    ploc_lat = np.append(latstr, latlon[0])
    ploc_lat.sort(); #ploc_lat = np.flip(ploc_lat)
    ploc_lon = np.append(lonstr, latlon[1])
    ploc_lon.sort(); #ploc_lon = np.flip(ploc_lon)
    plat_i = np.array(len(latstr))-np.where(ploc_lat == latlon[0]) #Had to correct Lat to get real values
    plon_i = np.where(ploc_lon == latlon[1])

    return (int(plat_i[0]), int(plon_i[0]))
