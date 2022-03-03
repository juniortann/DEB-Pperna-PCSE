import numpy as np
import matplotlib.pylab as plt
import matplotlib.patches as patches
import pickle
from xarray import open_dataset
from pandas import read_excel

# Georeferenced plotting
import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from scalebar import scale_bar #Imported code from the internet
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import ssl
ssl._create_default_https_context = ssl._create_unverified_context # for automatic shapefile download


# with open('NC_Data.pickle', 'rb') as f:
#     envdata = pickle.load(f)

with open('Result_PCSE_STD.pickle', 'rb') as f:
    result = pickle.load(f)
r_B = result['r_B']
L_i = result['L_i']


### Viewing yearly results
# var = 'CHL'
# for year in list(envdata[var].keys()):
#     plt.imshow(np.log(envdata[var][year]), cmap='rainbow')
#     plt.title(var+' '+year)
#     plt.savefig('Plots/'+var+'/'+var+'_'+year+'.png', facecolor='white')

# var = 'RB'
# for year in list(r_B.keys()):
#     plt.imshow(r_B[year], cmap='Spectral')
#     plt.title(var+' '+year)
#     plt.savefig('Plots/'+var+'/'+var+'_'+year+'.png', facecolor='white')
#
#
# var = 'LI'
# for year in list(L_i.keys()):
#     plt.imshow(L_i[year], cmap='bwr')
#     plt.title(var+' '+year)
#     plt.savefig('Plots/'+var+'/'+var+'_'+year+'.png', facecolor='white')


# Stack and Flatten the results
variable = r_B
years = variable.keys()
meanvariable = np.zeros(np.shape(variable['2002']))
for year in years:
    meanvariable = np.dstack((meanvariable, variable[year]))
meanvariable = np.delete(meanvariable, 0, 2) # Remove first layer of zeros
meanvariable[np.isnan(meanvariable)] = np.inf # clear possible residual nan's
rb_mean = np.nanmean(meanvariable, axis=2)


variable = L_i
years = variable.keys()
meanvariable = np.zeros(np.shape(variable['2002']))
for year in years:
    meanvariable = np.dstack((meanvariable, variable[year]))
meanvariable = np.delete(meanvariable, 0, 2) # Remove first layer of zeros
meanvariable[np.isnan(meanvariable)] = np.inf # clear possible residual nan's
L_i_mean = np.nanmean(meanvariable, axis=2)
# [np.nanmax(L_i[year]) for year in L_i.keys()]


#######################################################
### Load bathymetry, shapefiles and location points ###
#######################################################

# Bathymetry file
bat = open_dataset(r'bathymetry.nc')

# Load better resolution brazilian coastline shapefile
arquivo = shpreader.natural_earth(resolution='10m', category='cultural', name='admin_1_states_provinces')
# bathym = cfeature.NaturalEarthFeature(name='bathymetry_K_200', scale='10m', category='physical')
parser = shpreader.Reader(arquivo)

lat = np.array(result['lat'])
lon = np.array(result['lon'])

bat_lon, bat_lat, bathym = np.array(bat.lon), np.array(bat.lat), np.array(bat.elevation)

# Location points
locs = read_excel('Data_DiscussionSites.xlsx')
p_names = list(locs.Point)
p_lat = list(locs.Lat)
p_lon = list(locs.Lon)
p_lat = [float(p_lat[s].replace('°', '')) for s in range(len(p_lat))]
p_lon = [float(p_lon[s].replace('°', '')) for s in range(len(p_lon))]


#######################
### Actual ploting ###
######################

fig, ax = plt.subplots(1, 2, subplot_kw=dict(projection=ccrs.PlateCarree()), figsize=(13, 6.5))

# r_B plot
t2marketlength = rb_mean * 30 # cm/day to cm/month
paises = parser.records()

ax[0].add_feature(cfeature.OCEAN, facecolor = 'k')
ax[0].add_feature(cfeature.LAND, facecolor = 'k')
extent = [-49.5, -41.5, -29, -22.5]
ax[0].set_extent(extent)
for estado in paises:
    if estado.attributes['admin'] == 'Brazil':
        ax[0].add_geometries([estado.geometry], ccrs.PlateCarree(), facecolor='darkgray', edgecolor='k')
# Plotting location points
for i in range(len(p_lat)):
    ax[0].plot(p_lon[i], p_lat[i],  markersize=5, marker='o', color='white', markeredgecolor='k')
    ax[0].text(p_lon[i]-.09, p_lat[i]+.13, locs.Point[i], horizontalalignment='right', transform=ccrs.PlateCarree(),
        fontsize=11, color='white', weight='bold')
# Setting up gridlines
gl = ax[0].gridlines(draw_labels=True, linewidth=0.6, color='white', alpha=0.9)
gl.xlabels_top = False
gl.ylabels_right = False
gl.xlocator = mticker.FixedLocator([-52, -50, -48, -46, -44, -42, -40, -38])
gl.ylocator = mticker.FixedLocator([-21, -23, -25, -27, -29, -31])
gl.xlabel_style = {'size': 12}
gl.ylabel_style = {'size': 12}
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
# State name labels
ax[0].text(-42.7, -22.7, 'RJ', horizontalalignment='right', transform=ccrs.PlateCarree(),
        size='large', color='k')
ax[0].text(-47.5, -23.5, 'SP', horizontalalignment='right', transform=ccrs.PlateCarree(),
        size='large', color='k')
ax[0].text(-49, -25.4, 'PR', horizontalalignment='right', transform=ccrs.PlateCarree(),
        size='large', color='k')
ax[0].text(-49, -27.9, 'SC', horizontalalignment='right', transform=ccrs.PlateCarree(),
        size='large', color='k')
# Set scale bar (using scalebar.py, not cartopy)
text_kwargs = dict(size='large')
plot_kwargs = dict(linewidth=3.6)
scale_bar(ax[0], (0.8, 0.1), 100, text_kwargs=text_kwargs, plot_kwargs=plot_kwargs, color='k')
# North arrow
ax[0].arrow(-42.65, -27.5, 0, 0.2, linewidth=6, head_width=0.15, head_length=0.1,
        fc='k', ec='k', transform=ccrs.PlateCarree())
ax[0].text(-42.53, -27.93, 'N', horizontalalignment='right', transform=ccrs.PlateCarree(),
        fontsize = 15, weight='bold', color='k')
# Plot time to marketable length
im = ax[0].imshow(t2marketlength, cmap='Spectral_r', extent = (min(lon), max(lon), min(lat), max(lat)),
        transform=ccrs.PlateCarree())#, vmin = 3)
cbar = plt.colorbar(im, ax=ax[0], orientation="horizontal", shrink=.84, pad=.06) #ticks=range(9)
cbar.set_label('Growth coefficient (month$^{-1}$)', fontsize = 18, labelpad = 8)
#cbar.ax.tick_params(labelsize=15)
# Bathymetry
ax[0].contour(bat_lon, bat_lat, bathym, cmap = 'gray_r', levels=[-6000, -200],
            transform=ccrs.PlateCarree(), linewidths=1)
ax[0].text(-43.9, -24.9, '200m', horizontalalignment='right', transform=ccrs.PlateCarree(),
            fontsize = 10, color='k')
ax[0].text(-49.6, -30.5, '(A)', horizontalalignment='right', transform=ccrs.PlateCarree(),
            fontsize = 20, color='k')


# L_I
t2marketlength = L_i_mean
paises = parser.records()

ax[1].add_feature(cfeature.OCEAN, facecolor = 'k')
ax[1].add_feature(cfeature.LAND, facecolor = 'k')
extent = [-49.5, -41.5, -29, -22.5]
ax[1].set_extent(extent)
for estado in paises:
    if estado.attributes['admin'] == 'Brazil':
        ax[1].add_geometries([estado.geometry], ccrs.PlateCarree(), facecolor='darkgray', edgecolor='k')
# Plotting location points
for i in range(len(p_lat)):
    ax[1].plot(p_lon[i], p_lat[i],  markersize=5, marker='o', color='white', markeredgecolor='k')
    ax[1].text(p_lon[i]-.09, p_lat[i]+.13, locs.Point[i], horizontalalignment='right', transform=ccrs.PlateCarree(),
        fontsize=11, color='white', weight='bold')
# Setting up gridlines
gl = ax[1].gridlines(draw_labels=True, linewidth=0.6, color='white', alpha=0.9)
gl.xlabels_top = False
gl.ylabels_right = False
gl.xlocator = mticker.FixedLocator([-52, -50, -48, -46, -44, -42, -40, -38])
gl.ylocator = mticker.FixedLocator([-21, -23, -25, -27, -29, -31])
gl.xlabel_style = {'size': 10}
gl.ylabel_style = {'size': 10}
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
# State name labels
ax[1].text(-42.7, -22.7, 'RJ', horizontalalignment='right', transform=ccrs.PlateCarree(),
        size='large', color='k')
ax[1].text(-47.5, -23.5, 'SP', horizontalalignment='right', transform=ccrs.PlateCarree(),
        size='large', color='k')
ax[1].text(-49, -25.4, 'PR', horizontalalignment='right', transform=ccrs.PlateCarree(),
        size='large', color='k')
ax[1].text(-49, -27.9, 'SC', horizontalalignment='right', transform=ccrs.PlateCarree(),
        size='large', color='k')
# Set scale bar (using scalebar.py, not cartopy)
text_kwargs = dict(size='large')
plot_kwargs = dict(linewidth=3.6)
scale_bar(ax[1], (0.8, 0.1), 100, text_kwargs=text_kwargs, plot_kwargs=plot_kwargs, color='white')
# North arrow
ax[1].arrow(-42.65, -27.5, 0, 0.2, linewidth=6, head_width=0.15, head_length=0.1,
        fc='white', ec='white', transform=ccrs.PlateCarree())
ax[1].text(-42.53, -27.93, 'N', horizontalalignment='right', transform=ccrs.PlateCarree(),
        fontsize = 15, weight='bold', color='white')
# Plot time to marketable length
im = ax[1].imshow(t2marketlength, cmap='bwr', extent = (min(lon), max(lon), min(lat), max(lat)),
        transform=ccrs.PlateCarree(), vmax = 14)
cbar = plt.colorbar(im, ax=ax[1], orientation="horizontal", shrink=.84, pad=.06) #ticks=range(9)
cbar.set_label('Ultimate length (cm)', fontsize = 18, labelpad = 8)
#cbar.ax.tick_params(labelsize=15)
# Bathymetry
ax[1].contour(bat_lon, bat_lat, bathym, cmap = 'gray', levels=[-6000, -200],
            transform=ccrs.PlateCarree(), linewidths=1)
ax[1].text(-43.9, -24.9, '200m', horizontalalignment='right', transform=ccrs.PlateCarree(),
            fontsize = 10, color='white')

ax[1].text(-49.6, -30.5, '(B)', horizontalalignment='right', transform=ccrs.PlateCarree(),
            fontsize = 20, color='k')
fig.canvas.draw()
plt.tight_layout(pad=3.55)

plt.savefig('Plot_rblimean.tiff', dpi = 600, facecolor='white')
plt.savefig('Plot_rblimean.png', dpi = 600, facecolor='white')
plt.show()


##############################
### Plot Brazil study site ###
##############################

spec = 6
fig = plt.figure(figsize=(spec*1.6, spec), dpi=600)
gs = fig.add_gridspec(10, 15)
ax0 = fig.add_subplot(gs[:, 0:5], projection=ccrs.PlateCarree())
ax1 = fig.add_subplot(gs[:, 6:], projection=ccrs.PlateCarree())

arquivo = shpreader.natural_earth(resolution='10m', category='cultural', name='admin_1_states_provinces')
parser = shpreader.Reader(arquivo)
paises = parser.records()

extent = [-65, -35, 6, -35]
ax0.set_extent(extent)

gl = ax0.gridlines(draw_labels=True, linewidth=0.6, color='white', alpha=0.1)
gl.xlabels_top = False
gl.ylabels_right = False
gl.xlocator = mticker.FixedLocator([-60, -50,-40])
gl.xlabel_style = {'size': 10}
gl.ylabel_style = {'size': 10}
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

ax0.add_feature(cfeature.OCEAN, facecolor = 'k')#'darkblue', alpha=.3)
ax0.add_feature(cfeature.LAND, facecolor = 'k', alpha=.6)
ax0.add_feature(cfeature.BORDERS)

# plt.imshow(r_B_mean, cmap = 'rainbow', extent = (min(lon), max(lon), min(lat), max(lat)),
#            vmin=0.0023150968055078982, vmax=0.004467200519169916, transform=ccrs.PlateCarree())

# Add country label
ax0.text(-45, -15, 'Brazil', horizontalalignment='right', transform=ccrs.PlateCarree(), fontsize=20, color='white')

# Add rectangle
rect = patches.Rectangle((np.min(lon),np.min(lat)),np.max(lon)-np.min(lon),np.max(lat)-np.min(lat),linewidth=3,edgecolor='orange',facecolor='none')
ax0.add_patch(rect)

# Set scale bar (using scalebar.py, not cartopy)
text_kwargs = dict(size='small')
plot_kwargs = dict(linewidth=3.6)
scale_bar(ax0, (0.7, 0.07), 500, text_kwargs=text_kwargs, plot_kwargs=plot_kwargs, color='white')

# North arrow
ax0.arrow(-40, 1, 0, 1, linewidth=5, head_width=0.4, head_length=0.3,
          fc='white', ec='white', transform=ccrs.PlateCarree())
ax0.text(-39.3, -1.5, 'N', horizontalalignment='right', transform=ccrs.PlateCarree(),
         fontsize = 10, weight='bold', color='white')


### Locations ###
paises = parser.records()
color = 'orange'

ax1.add_feature(cfeature.OCEAN, facecolor = 'k')
ax1.add_feature(cfeature.LAND, facecolor = 'k')
extent = [-49.5, -41.5, -29, -22.5]
ax1.set_extent(extent)
for estado in paises:
    if estado.attributes['admin'] == 'Brazil':
        ax1.add_geometries([estado.geometry], ccrs.PlateCarree(), facecolor='darkgray', edgecolor='k')
# Plotting location points
for i in range(len(p_lat)):
    ax1.plot(p_lon[i], p_lat[i],  markersize=5, marker='o', color=color, markeredgecolor='k')
    ax1.text(p_lon[i]-.09, p_lat[i]+.13, locs.Point[i], horizontalalignment='right', transform=ccrs.PlateCarree(),
        fontsize=8.5, color='white', weight='bold')
# Setting up gridlines
gl = ax1.gridlines(draw_labels=True, linewidth=0.6, color='white', alpha=0.9)
gl.xlabels_top = False
gl.ylabels_right = False
gl.xlocator = mticker.FixedLocator([-52, -50, -48, -46, -44, -42, -40, -38])
gl.ylocator = mticker.FixedLocator([-21, -23, -25, -27, -29, -31])
gl.xlabel_style = {'size': 10}
gl.ylabel_style = {'size': 10}
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
# State name labels
plt.text(-42.7, -22.7, 'RJ', horizontalalignment='right', transform=ccrs.PlateCarree(),
        size='medium', color='k', weight='bold')
plt.text(-47.5, -23.5, 'SP', horizontalalignment='right', transform=ccrs.PlateCarree(),
        size='medium', color='k', weight='bold')
plt.text(-49, -25.4, 'PR', horizontalalignment='right', transform=ccrs.PlateCarree(),
        size='medium', color='k', weight='bold')
plt.text(-49, -27.9, 'SC', horizontalalignment='right', transform=ccrs.PlateCarree(),
        size='medium', color='k', weight='bold')
# Set scale bar (using scalebar.py, not cartopy)
text_kwargs = dict(size='small')
plot_kwargs = dict(linewidth=3.6)
scale_bar(ax1, (0.8, 0.1), 100, text_kwargs=text_kwargs, plot_kwargs=plot_kwargs, color='white')
# North arrow
ax1.arrow(-42.6, -27.55, 0, 0.2, linewidth=6, head_width=0.15, head_length=0.1,
          fc='white', ec='white', transform=ccrs.PlateCarree())
ax1.text(-42.45, -28, 'N', horizontalalignment='right', transform=ccrs.PlateCarree(),
         fontsize = 15, weight='bold', color='white')
# Bathymetry
ax1.contour(bat_lon, bat_lat, bathym, cmap = 'gray', levels=[-6000, -200],
            transform=ccrs.PlateCarree(), linewidths=1)
ax1.text(-43.9, -24.9, '200m', horizontalalignment='right', transform=ccrs.PlateCarree(),
            fontsize = 8, color='white')

fig.canvas.draw()
plt.tight_layout(pad=3.55)
plt.savefig('Plot_StudySite.tiff', dpi = 600, facecolor='white')
plt.savefig('Plot_StudySite.png', dpi = 600, facecolor='white')
plt.show()
