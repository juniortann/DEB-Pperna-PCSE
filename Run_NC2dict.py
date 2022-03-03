import NCtools as nc
import pickle

# Create dictionary with netCDF data
l = ['NC_CHL', 'NC_SST', 'NC_PIC'] # List of folders
envdata = nc.nc_mergedicts(l)
with open('NC_Data.pickle', 'wb') as f:
    pickle.dump(envdata, f)
