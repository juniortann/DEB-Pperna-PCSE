from sklearn.metrics import mean_squared_error
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
file = 'results_Perna_perna.mat'
pars = DEB.get_pars(file)
for key, val in pars.items():         # Varspull
    exec(key + '=val')


### ACTUAL SIMULATION ###

# Initial variables to get characretistics of data
var_0 = list(envdata.keys())[0]
year_0 = list(envdata[var_0].keys())[0]
shape = envdata[var_0][year_0].shape

# Empty dictionary to store data
r_B = dict()
L_i = dict()

for i in range(len(envdata[var_0])):
    years = list(envdata[var_0].keys())

    for year in years:
        r_B[year] = np.zeros(shape)  # Prelocating
        L_i[year] = np.zeros(shape)
        lines = range(shape[0])  # Number of lines
        columns = range(shape[1])  # Number of columns
        for l in lines: # Should have used enumerate
            for c in columns:  # index[line, column]
                X = envdata['CHL'][year][l, c]
                Y = envdata['POC'][year][l, c]
                f = DEB.f_POC(X, Y, X_K, Y_K, c_chl)
                T = envdata['SST'][year][l, c]
                if f < 0.01:  # f_min in DEBTool for reaching E_Hb
                    r_B[year][l][c] = np.nan
                    L_i[year][l][c] = np.nan
                else:
                    r_B[year][l][c], L_i[year][l][c] = DEB.rb_li(f, T, pars)


# Save output
results = envdata
l_key = ['r_B', 'L_i']
l_key.append(list(envdata.keys()))
results['r_B'] = r_B
results['L_i'] = L_i

results['lat'] = coords['lat']
results['lon'] = coords['lon']

with open('Result_PCSE_STD.pickle', 'wb') as f:
    pickle.dump(results, f)

# Viewing results
plt.imshow(np.log(envdata['CHL']['2002']), cmap='rainbow')  # chl conditions
plt.imshow(np.log(envdata['SST']['2002']), cmap='inferno')  # SST conditions

plt.imshow(r_B['2010'], cmap='Spectral')  # r_B
plt.imshow(L_i['2010'], cmap='bwr')  # L_i


# Simulating data for SP3 using site temperature
def growth(L0, Li, rb, t):
    """von Bertalanffy growth"""
    return Li - (Li - L0) * np.exp(-rb * t)


def var_value(data, var, year, loc):
    """Returns value for pixel in dict."""
    return data[var][year][loc]


time_SP3, l_SP3 = ([  # time settlement (months), length (mm)
    3.3012, 4.2864, 5.1984, 6.2244, 7.1736, 8.2032, 9.2244, 10.2468, 11.1624, 12.2208, 13.17, 14.1948, 15.144, 16.2024, 2.7792, 3.846, 4.8384, 5.8308, 6.8232, 7.8156, 8.8092, 9.7284, 10.794, 11.7864, 12.7428, 4.0272, 4.8336, 5.8608, 6.8136, 7.914, 8.8308, 9.822, 10.7388, 11.8392, 12.8652, 13.746, 14.7732, 15.7992, 16.68, 17.7804],
    [
    9.92, 9.7085, 9.8727, 13.7723, 13.5618, 22.1342, 21.735, 21.8964, 25.7988, 25.7724, 26.1226, 29.8354, 29.8117, 29.9723, 5.8847, 5.7094, 9.8728, 18.3759, 18.3884, 22.1744, 26.5266, 26.3494, 22.2119, 22.2244, 26.7647, 9.8356, 10.1273, 9.737, 14.0647, 18.2018, 22.1525, 21.9514, 22.1285, 25.6996, 25.8754, 25.8643, 30.0023, 29.612, 30.3557, 29.9645
])
time_SP3 = np.array(time_SP3)*30

year_SP3 = list(envdata[var_0].keys())
iSP3 = (63, 156)  # Ubatuba
chl = np.mean([var_value(envdata, 'CHL', year, iSP3) for year in year_SP3])
sst = np.mean([var_value(envdata, 'SST', year, iSP3) for year in year_SP3])
poc = np.mean([var_value(envdata, 'POC', year, iSP3) for year in year_SP3])

temp = 18.8

f = DEB.f_POC(chl, poc, X_K, Y_K, c_chl)
rb_remote, li_remote = DEB.rb_li(f, sst, pars)
rb_paper, li_paper = DEB.rb_li(f, temp, pars)
print(rb_paper, li_paper)

l_remote = growth(0, li_remote, rb_remote, time_SP3)
l_paper = growth(0, li_paper, rb_paper, time_SP3)

error_remote = mean_squared_error(np.array(l_SP3)/10, l_remote, squared=False)
error_paper = mean_squared_error(np.array(l_SP3)/10, l_paper, squared=False)

print(error_remote, error_paper)


plt.scatter(time_SP3/30, np.array(l_SP3)/10)
plt.scatter(time_SP3/30, l_remote, c='green')
plt.scatter(time_SP3/30, l_paper, c='red')
plt.legend(['field', 'remote', 'paper'])
