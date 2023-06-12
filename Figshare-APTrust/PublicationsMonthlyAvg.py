"""
Created on Mon Mar 07 09:41:18 2023

@author: padma carstens
"""
"""
Purpose: 

-Reads the publication dates from 2022 spreadsheet 
-Plots the number of publications agregated each month vs the month
-Overplots the rolling mean of publications over 5 month period vs the month. See the plot RollingMean5MonthPeriodPublicationsVsDate.jpeg

"""


import os
import sys
from os.path import exists
import pandas as pd
sys.path.append('VTechDataRepo\APTrustBagTransferAndmd5Verification')
import json
from turtle import begin_fill
#import spreadsheet_aptrust_transfer
from spreadsheet_aptrust_transfer import aptrust_vtingsheet
from spreadsheet_aptrust_transfer import aptrust_vtpubsheet
from datetime import datetime
Pvtsheet=aptrust_vtpubsheet()
pDate=Pvtsheet['pDate']
print(pDate)
dateYMDs=[]
pDates=pDate[1:len(pDate)]
months=[]
for z in pDates:
    ##print('z is ',z)
    #print('Date for this is ')
    dateYMD = datetime.strptime(z, '%Y%m%d').strftime('%Y'+'-'+'%m'+'-'+'%d')
    month = datetime.strptime(z, '%Y%m%d').strftime('%m')    
    #dateYMDs=dateYMDs.append(dateYMD)
    dateYMDs.append(dateYMD)
    months.append(month)


a=[1]*len(pDates)
#print(dateYMDs)
#print(months)

d={'dates':dateYMDs,'PublicationsPerMonth':a}
#dm={'months':months,'Publications':a}
#print(d)
#print(dm)

df=pd.DataFrame(d)
#print(df)
df['month']=pd.DatetimeIndex(df['dates']).month
df['year']=pd.DatetimeIndex(df['dates']).year

years=df['year']
months=df['month']

import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
  
# using Series.plot() method
#gfg = pd.Series([0.1, 0.4, 0.16, 0.3, 0.9, 0.81])
#--------------------------------------------One way of plotting this
#ms.plot()
##ms.plot('YYYY,MM','NumberOfPublications')
#plt.show()
s=df.groupby([years,months])['PublicationsPerMonth'].sum()

#Rolling average
#s5=df.groupby([years,months])['Publications'].rolling(2).mean()
q=pd.DataFrame(s)
q['RollingMean_5MonthPeriod']=q['PublicationsPerMonth'].rolling(5).mean()

#s5=df.groupby([years,months]).rolling(2).['Publications'].mean()
#s=s5.iloc[::5,:]

#s.plot(kind='bar',xlabel= 'Date(YYYY,MM)',ylabel= 'Number of Publications',fontsize=8)
q.plot(kind='bar',xlabel= 'Date(YYYY,MM)',ylabel= 'Number of Publications',fontsize=8)

#plt.plot(s)
#plt.plot(vx)
plt.show()
#----------------------------
#df['date'] = df['year'].map(str)+ '-' +df['year'].map(str)
#df['date'] = pd.to_datetime(df['date'], format='%m-%Y').dt.strftime('%m-%Y')
#fig, ax = plt.subplots()
#plt.plot_date(df['date'], df['Value'])
#plt.show()
#-----------------------------------
#import matplotlib
#import matplotlib.pyplot as plot
#s=df.groupby([years,months])['Publications'].sum()
#plot_df=s.unstack('month').loc[:]
#plot_df.index = pd.PeriodIndex(plot_df.index.tolist(), freq='a')
#plot_df.plot()
#-------------------------

#import matplotlib
#matplotlib.style.use('ggplot')
#import matplotlib.pyplot as plt

#plt.figure()
#df.groupby([years,months])['Publications'].sum().unstack().plot()



