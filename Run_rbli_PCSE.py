import numpy as np
import matplotlib.pylab as plt
import DEB_functions as DEB
import pickle


# Open pickled dictionary with .nc data
with open('NC_Data.pickle', 'rb') as f:
    envdata = pickle.load(f)

# Extract parameters
file = 'results_Perna_perna.mat'
pars = DEB.get_pars(file)
for key, val in pars.items():         # Varspull
    exec(key + '=val')

# Ready funcional response equation parameters
# Estimated from SP-03 (Ubatuba) data OLS w/ (Marques et al, 1991) & yearly PIC max
X_K = 1.545
Y_K = 0.002  # Max SP-03 POC values

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
        for l in lines:
            for c in columns:  # index[line, column]
                X = envdata['CHL'][year][l, c]
                Y = envdata['PIC'][year][l, c]
                f = DEB.f_PIC(X, Y, X_K, Y_K)
                T = envdata['SST'][year][l, c]
                if f < 0.162:  # E_b_min in DEBTool
                    r_B[year][l][c] = np.nan
                    L_i[year][l][c] = np.nan
                else:
                    r_B[year][l][c], L_i[year][l][c] = DEB.rb_li(f, T, pars)


results = envdata
l_key = ['r_B', 'L_i']
l_key.append(list(envdata.keys()))
results['r_B'] = r_B
results['L_i'] = L_i


# with open('Result_PCSE_.pickle', 'wb') as f:
#     pickle.dump(results, f)
#
# # Save output
# with open('Result_rB_PCSE_.pickle', 'wb') as f:
#     pickle.dump(r_B, f)
#
# with open('Result_Li_PCSE.pickle', 'wb') as f:
#     pickle.dump(L_i, f)

# Viewing results
plt.imshow(np.log(envdata['CHL']['2002']),
           cmap='rainbow')  # chlor-a conditions
plt.imshow(np.log(envdata['SST']['2002']), cmap='inferno')  # SST conditions

plt.imshow(r_B['2010'], cmap='Spectral')  # r_B
plt.imshow(L_i['2010'], cmap='bwr')  # L_i
