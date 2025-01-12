"""
Purpose: 
read netcdf .nc files and plot /print arrays shown in comments at the bottom
"""

import numpy as np
import netCDF4 as nc
#import netcdf as nc
from netCDF4 import Dataset
#from netcdf import Dataset

#fn = 'C:/Users/padma/Anaconda3/envs/curation/cips_raa_2a_orbit_86237_2023-008_v01.10_r06_cat.preliminary.nc'
fn='C:/Users/padma/anaconda3/envs/curation/VTDR_I00278/SABER_NH_GWamplitude_v0.nc'
ds = nc.Dataset(fn)
print(ds)#,"                                                     ")
fn1='C:/Users/padma/anaconda3/envs/curation/VTDR_I00278/SABER_NH_Temperature_v0.nc'
ds1 = nc.Dataset(fn1)
print(ds1)
#print(ds[YEAR])
#print(ds['VERSION'])
#f = netCDF4.Dataset('C:/Users/padma/Anaconda3/envs/curation/cips_raa_2a_orbit_86237_2023-008_v01.10_r06_cat.preliminary.nc')
#examples of plotting ncdf data from the variables
#################################################################
#import matplotlib.pyplot as plt
#x=ds.variables['YEAR'][:] 
#plt.plot(x)
#plt.plot(x,'ro') 
#plt.show()

#x1=ds.variables['Z'][:]    
#plt.plot(x1,'ro') 
#plt.show()

#x2=ds.variables['DOY']   
#plt.plot(x2)
#plt.show()  
#k1=ds1.variables['NY'][:]
#plt.plot(k1,'ro') 
#plt.show()
#print(ds.variables['GWamp'][:,10,10]) #print instead of plotting 3D since this probably requires for loops to get all dimenstions on 3D plot

#k2=ds1.variables['Z'][:]
#plt.plot(k2,'ro') 
#plt.show()
#k3=ds1.variables['DOY']
#plt.plot(k3,'ro') 
#plt.show()
#########################################################################
"""
type(ds)
type(ds.variables)
ds.variables
ds.variables['YEAR"]
ds.variables['YEAR'][0] 
masked_array(data=2003,
             mask=False,
       fill_value=999999)
ds.variables['YEAR'][0:79] 
masked_array(data=[2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011,
                   2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
             mask=False,
       fill_value=999999)
ds.variables['YEAR'][:]    
masked_array(data=[2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011,
                   2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
             mask=False,
       fill_value=999999)




-----------------------

ds1
ds1.dimensions
ds1.dimensions['NZ']
#above are only dimension description not values
#below are checking for values

print(ds1.variables['TEMPERATURE'][:,10,10])
"""