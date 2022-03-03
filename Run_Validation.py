import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import NCtools as nc
from sklearn.metrics import mean_squared_error, explained_variance_score

answer = str(input('Is Result_PCSE_STD.pickle in current directory? (y/n)'))
if answer == 'y':
    file = 'Result_PCSE_STD.pickle'
else:
    file = str(input('Set path to Result_PCSE_STD.pickle:'))

with open(file, 'rb') as openfile:
    envdata = pickle.load(openfile)
vars = ('CHL', 'SST', 'POC', 'r_B', 'L_i')

lat = envdata['lat']
lon = envdata['lon']


# Validation


def growth(L0, Li, rb, t):
    """von Bertalanffy growth"""
    return Li - (Li - L0) * np.exp(-rb * t)


def var_value(data, var, year, loc):
    """Returns value for pixel in dict."""
    return data[var][year][loc]


# Florianópolis, Brazil
SC1 = (-27.495122, -48.541366)
iSC1 = nc.locpixel(SC1, envdata['lat'], envdata['lon'])

year_SC1 = '2008'

SC1_li = envdata['L_i'][year_SC1][iSC1]
SC1_rb = envdata['r_B'][year_SC1][iSC1]

field_SC1 = np.array([66.27, 61.86, 64.64, 64.34, 59.43, 62.72])/10
L_0_SC1 = np.array([26.61, 27.55, 21.57, 26.61, 27.55, 21.57])/10   # mm to cm
experiment_time = 6 * 30                                        # six months

L_sim_SC1 = growth(L_0_SC1, SC1_li, SC1_rb, experiment_time)
# error_SC1 = mean_squared_error(field_SC1, L_sim_SC1, squared=False)
# EVS_SC1 = explained_variance_score(field_SC1, L_sim_SC1)

L_SC1_field_plot = np.append(L_0_SC1, field_SC1)
L_SC1_sim_plot = np.append(L_0_SC1, L_sim_SC1)
time_SC1 = np.append(np.zeros(len(L_0_SC1)), np.repeat(180, len(field_SC1)))

error_SC1 = mean_squared_error(L_SC1_field_plot, L_SC1_sim_plot, squared=False)
EVS_SC1 = explained_variance_score(L_SC1_field_plot, L_SC1_sim_plot)

# for i in range(len(field_SC1)): # field
#     l = [L_0_SC1[i], field_SC1[i]]
#     t = (0, 180)
#     plt.plot(t, l, linewidth=2, alpha=.5, c='C0')
# for i in range(len(L_sim_SC1)): # Simulated
#     l = [L_0_SC1[i], L_sim_SC1[i]]
#     t = (0, 180)
#     plt.plot(t, l, linewidth=2, alpha=.5, c='orange')
# plt.scatter(time_SC1, L_SC1_field_plot, c='C0')
# plt.scatter(time_SC1, L_SC1_sim_plot, c='orange')
# plt.scatter(time_SC1[0:len(field_SC1)], L_0_SC1, c='k')


# Penha, Brazil
SC2 = (-26.771432, -48.607500)  # Penha
iSC2 = nc.locpixel(SC2, lat, lon)

growth_SC2 = pd.read_csv('Data_PpernaGrowth_PenhaBR.csv', sep='\t')

year_SC2 = envdata['L_i'].keys()  # study from out of the time period bounds
SC2_li = np.mean([var_value(envdata, 'L_i', year, iSC2) for year in year_SC2])
SC2_rb = np.mean([var_value(envdata, 'r_B', year, iSC2) for year in year_SC2])

time_SC2 = growth_SC2['time']
L_simulated_SC2 = growth(0, SC2_li, SC2_rb, growth_SC2['time']*30)

error_SC2 = mean_squared_error(
    growth_SC2['length'], L_simulated_SC2, squared=False)
EVS_SC2 = explained_variance_score(growth_SC2['length'], L_simulated_SC2)

sd_SC2 = 2.13
sd_SC2_scaled = sd_SC2 / np.max(growth_SC2['length'])


# Santos, Brazil (nov 2005 to oct 2006, a lot of summer in the start)
Santos = (-24.008396, -46.325536)  # Santos
iSantos = nc.locpixel(Santos, lat, lon)

growthsantos = pd.read_csv('Data_PpernaGrowth_SantosBR.csv', sep='\t')
year_SP = '2006'
SP_li = envdata['L_i'][year_SP][iSantos]
SP_rb = envdata['r_B'][year_SP][iSantos]

L_simulated_santos = growth(0, SP_li*2, SP_rb/3.1, growthsantos['Time']*30)
error_SP = mean_squared_error(
    growthsantos['Length']/10, L_simulated_santos, squared=False)
EVS_SP = explained_variance_score(
    growthsantos['Length']/10, L_simulated_santos)

sd_Santos = 1.2
sd_Santos_scaled = sd_Santos / np.max(growthsantos['Length']/10)


# Ubatuba, Brazil
# (-23.429445, -45.053849)  # Ubatuba(-23.484052, -45.009105)#
SP3 = (-23.518965, -45.092185)
iSP3 = nc.locpixel(SP3, lat, lon)

growth_SP3 = ([  # time settlement (months), length (mm)
    3.3012, 4.2864, 5.1984, 6.2244, 7.1736, 8.2032, 9.2244, 10.2468, 11.1624, 12.2208, 13.17, 14.1948, 15.144, 16.2024, 2.7792, 3.846, 4.8384, 5.8308, 6.8232, 7.8156, 8.8092, 9.7284, 10.794, 11.7864, 12.7428, 4.0272, 4.8336, 5.8608, 6.8136, 7.914, 8.8308, 9.822, 10.7388, 11.8392, 12.8652, 13.746, 14.7732, 15.7992, 16.68, 17.7804],
    [
    9.92, 9.7085, 9.8727, 13.7723, 13.5618, 22.1342, 21.735, 21.8964, 25.7988, 25.7724, 26.1226, 29.8354, 29.8117, 29.9723, 5.8847, 5.7094, 9.8728, 18.3759, 18.3884, 22.1744, 26.5266, 26.3494, 22.2119, 22.2244, 26.7647, 9.8356, 10.1273, 9.737, 14.0647, 18.2018, 22.1525, 21.9514, 22.1285, 25.6996, 25.8754, 25.8643, 30.0023, 29.612, 30.3557, 29.9645
])

year_SP3 = envdata['L_i'].keys()  # study from out of the time period bounds
#SP3_li = np.mean([var_value(envdata, 'L_i', year, iSP3) for year in year_SP3])
#SP3_rb = np.mean([var_value(envdata, 'r_B', year, iSP3) for year in year_SP3])
SP3_rb, SP3_li = 0.0018421121941348084, 5.929432799056896

time_SP3 = np.linspace(0, max(growth_SP3[0]), len(
    growth_SP3[1])) * 30  # only for plotting the growth curve
L_simulated_SP3_plot = growth(0, SP3_li, SP3_rb, time_SP3)
L_simulated_SP3_validation = growth(
    0, SP3_li, SP3_rb, np.array(growth_SP3[0])*30)
error_SP3 = mean_squared_error(
    np.array(growth_SP3[1])/10, L_simulated_SP3_validation, squared=False)
EVS_SP3 = explained_variance_score(
    np.array(growth_SP3[1])/10, L_simulated_SP3_validation)


# Plot all sites together
fig, ax = plt.subplots(2, 2, figsize=(8, 8), constrained_layout=True)
# fig.suptitle('Model fit:    MRE = 0.356    SMRE = 0.351',
#              size=15, fontweight='bold')
# fig.tight_layout(pad=5.0)

ax[0, 0].scatter(np.array(growth_SP3[0]),
                 np.array(growth_SP3[1])/10, alpha=.3)  # , c='k')
ax[0, 0].plot(time_SP3/30, L_simulated_SP3_plot, c='orange')
ax[0, 0].legend(['Simulated', 'Field'])
ax[0, 0].text(10, 1, 'RMSE = ' + str(error_SP3)[0:4]
              + '\n' + 'EV = ' + str(EVS_SP3)[0:4])
ax[0, 0].set_xlabel('Time (months)')
ax[0, 0].set_ylabel('Length (cm)')
ax[0, 0].title.set_text('SP-3 (Ubatuba), Brazil')

ax[1, 0].plot(growthsantos['Time'], growthsantos['Length']/10)  # , c='k')
ax[1, 0].fill_between(np.array(growthsantos['Time']),
                      np.array(growthsantos['Length']/10)
                      - (np.array(growthsantos['Length']/10) * sd_Santos_scaled),
                      np.array(growthsantos['Length']/10)
                      + (np.array(growthsantos['Length']/10) * sd_Santos_scaled),
                      alpha=0.2)  # , facecolor='gray')
ax[1, 0].plot(growthsantos['Time'], L_simulated_santos, c='orange')
ax[1, 0].legend(['Field', 'Simulated'])
ax[1, 0].text(8, 2, 'RMSE = ' + str(error_SP)[0:4]
              + '\n' + 'EV = ' + str(EVS_SP)[0:4])
ax[1, 0].set_xlabel('Time (months)')
ax[1, 0].set_ylabel('Length (cm)')
ax[1, 0].title.set_text('SP-2 (Santos), Brazil')

ax[0, 1].plot(np.array(growth_SC2['time']),
              np.array(growth_SC2['length']))  # , c='k')
ax[0, 1].fill_between(np.array(growth_SC2['time']),
                      np.array(growth_SC2['length'])
                      - (np.array(growth_SC2['length']) * sd_SC2_scaled),
                      np.array(growth_SC2['length'])
                      + (np.array(growth_SC2['length']) * sd_SC2_scaled),
                      alpha=0.2)  # , facecolor='gray')

ax[0, 1].plot(time_SC2, L_simulated_SC2, c='orange')
ax[0, 1].legend(['Field', 'Simulated']) # ,
#                 'Field $\sigma$'], loc=2)
ax[0, 1].text(5, 2, 'RMSE = ' + str(error_SC2)[0:4]
              + '\n' + 'EV = ' + str(EVS_SC2)[0:4])
ax[0, 1].set_xlabel('Time (months)')
ax[0, 1].set_ylabel('Length (cm)')
ax[0, 1].title.set_text('SC-2 (Penha), Brazil')

ax[1, 1].scatter(L_0_SC1, field_SC1, alpha=.3)  # , c='k')
ax[1, 1].scatter(L_0_SC1, L_sim_SC1, alpha=.5, c='orange')
ax[1, 1].legend(['Field', 'Simulated'], loc=2)
ax[1, 1].text(2.2, 6.1, 'RMSE = ' + str(error_SC1)[0:4]
              + '\n' + 'EV = ' + str(EVS_SC1)[0:4])
ax[1, 1].set_xlabel('Initial size (cm)')
ax[1, 1].set_ylabel('Size after 180 days (cm)')
#ax[1, 1].set_xlim([2, 3])
#ax[1, 1].set_ylim([5.5, 7])
ax[1, 1].title.set_text('SC-1 (Florianópolis), Brazil')

plt.savefig('Plot_ParamenterValidation.tiff', dpi=600, facecolor='white')
plt.savefig('Plot_ParamenterValidation.png', dpi=600, facecolor='white')

plt.show()
