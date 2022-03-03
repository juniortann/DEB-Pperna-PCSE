import numpy as np
import matplotlib.pylab as plt
import DEB_functions_STD as DEB
import pickle


# Open pickled dictionary with .nc data
with open('NC_Data.pickle', 'rb') as f:
    envdata = pickle.load(f)
with open('NC_LatLon.pickle', 'rb') as f:
    coords = pickle.load(f)

# Extract parameters
file = 'results_Perna_perna_STD_no_POC.mat'
pars = DEB.get_pars(file)
for key, val in pars.items():         # Varspull
    exec(key + '=val')

# Ready funcional response equation parameters
C_chlor = 52  # https://www.scielo.br/j/bjoce/a/MHMcqnMF9XC3WpKvRM6mgcC/?format=pdf&lang=en 12.8 Carbon:chlor ratio for the region, from Bucci, 2010
# X_K = 1.205
# Y_K = 150.2

### ACTUAL SIMULATION ###

# Initial variables to get characretistics of data
var_0 = list(envdata.keys())[0]
year_0 = list(envdata[var_0].keys())[0]
shape = envdata[var_0][year_0].shape

# Empty dictionary to store data
r_B = dict()
L_i = dict()

for i in range(len(envdata[var_0])):
    years = ['2009', '2010']  # list(envdata[var_0].keys())

    for year in years:
        r_B[year] = np.zeros(shape)  # Prelocating
        L_i[year] = np.zeros(shape)
        lines = range(shape[0])  # Number of lines
        columns = range(shape[1])  # Number of columns
        for l in lines: # Should have used enumerate
            for c in columns:  # index[line, column]
                X = envdata['CHL'][year][l, c]
                Y = envdata['POC'][year][l, c]
                f = X / (X + X_K)
                T = envdata['SST'][year][l, c]
                if f < 0.01:  # f_min in DEBTool for reaching E_Hb
                    r_B[year][l][c] = np.nan
                    L_i[year][l][c] = np.nan
                else:
                    r_B[year][l][c], L_i[year][l][c] = DEB.rb_li(f, T, pars)


results = envdata
l_key = ['r_B', 'L_i']
l_key.append(list(envdata.keys()))
results['r_B'] = r_B
results['L_i'] = L_i

results['lat'] = coords['lat']
results['lon'] = coords['lon']

# with open('Result_PCSE_STD.pickle', 'wb') as f:
#     pickle.dump(results, f)
#
# # Save output
# with open('Result_rB_PCSE_STD.pickle', 'wb') as f:
#     pickle.dump(r_B, f)
#
# with open('Result_Li_PCSE_STD.pickle', 'wb') as f:
#     pickle.dump(L_i, f)

# Viewing results
plt.imshow(np.log(envdata['CHL']['2002']),
           cmap='rainbow')  # chlor-a conditions
plt.imshow(np.log(envdata['SST']['2002']), cmap='inferno')  # SST conditions

plt.imshow(r_B['2010'], cmap='Spectral')  # r_B
plt.imshow(L_i['2010'], cmap='bwr')  # L_i


# Validation

def locpixel(latlon, lat, lon):
    """
    Locate the pixel index from geographic coordinates.

    Args:
     - latlon = list with [latitude, longitude] of interest
     - lat = list of latitudes from data
     - lon = list of longitude from data

    Returns:
     - (latitute index, longitude index)

    """

    ploc_lat = np.append(lat, latlon[0])
    ploc_lat.sort()  # ploc_lat = np.flip(ploc_lat)
    ploc_lon = np.append(lon, latlon[1])
    ploc_lon.sort()  # ploc_lon = np.flip(ploc_lon)
    # Had to correct Lat to get real values
    plat_i = np.array(len(lat))-np.where(ploc_lat == latlon[0])
    plon_i = np.where(ploc_lon == latlon[1])

    return (int(plat_i[0]), int(plon_i[0]))


def growth(L0, Li, rb, t):
    """von Bertalanffy growth"""
    return Li - (Li - L0) * np.exp(-rb * t)


SC1 = [-27.483333, -48.55]
iSC1 = locpixel(SC1, envdata['lat'], envdata['lon'])

year_SC1 = '2009'

SC1_li = envdata['L_i'][year_SC1][iSC1]
SC1_rb = envdata['r_B'][year_SC1][iSC1]

field = np.array([66.27, 61.86, 64.64, 64.34, 59.43, 62.72])/10
L_0 = np.array([26.61, 27.55, 21.57, 26.61, 27.55, 21.57])/10   # mm to cm
experiment_time = 6 * 30                                        # six months

L_simulated = growth(L_0, SC1_li, SC1_rb, experiment_time)

print(L_simulated)

plt.scatter(field, L_simulated)


# Change the .mat to what is was and try again
