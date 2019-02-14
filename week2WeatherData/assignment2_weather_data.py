# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 16:58:26 2019

@author: 121b2
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#loading the data
df = pd.read_csv('dataWeather.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df[df['Date'].apply(lambda x: (x.day, x.month))!=(29,2)] #excluding the leap year, i.e. 29-02

#test plot
#plt.figure()
#plt.plot(df['Date'][:400],df['Data_Value'][:400],'.g')
##

df2=(df.set_index('Date')[:'2014']);df2.reset_index() #creating period 2005-2014
df3 =(df.set_index('Date')['2015']) #creating period year 2015

monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

#anonymous functions
xx = lambda x: (x.day,x.month)
yy = lambda y: pd.to_datetime(str(y[0])+'-'+str(monthDict[y[1]])+'-2015')

#finding the min/max temperatures for the period 2005-2014
x1 = .1*df2['Data_Value'].groupby(by=xx(df2.index)).min()
x2 = .1*df2['Data_Value'].groupby(by=xx(df2.index)).max()
#finding the min/max teperatures for the 2015
x3 = .1*df3['Data_Value'].groupby(by=xx(df3.index)).min()
x4 = .1*df3['Data_Value'].groupby(by=xx(df3.index)).max()

#creating a data frame
df_ans = pd.concat([x1,x2,x3,x4],axis=1)

df_ans['date'] = list(map(yy,df_ans.index))

df_ans = df_ans.set_index(df_ans['date'])

df_ans.columns = ['min', 'max', 'min2015', 'max2015', 'date']

df_ans = df_ans.sort_index()

#creating the excess temperatures for 2015
df_ans['excessMin'] = df_ans.apply(lambda row: row['min2015'] if (row['min2015'] < row['min']) else np.nan, axis = 1)
df_ans['excessMax'] = df_ans.apply(lambda row: row['max2015'] if (row['max2015'] > row['max']) else np.nan, axis = 1)

###plotting
plt.figure()
plt.plot(df_ans.iloc[:,0],'lightblue',label = 'min temperature for the period 2005-2014')
plt.plot(df_ans.iloc[:,1],'pink',label = 'max temperature for the period 2005-2014')

plt.gca().fill_between(df_ans.iloc[:,0].index, 
                       df_ans.iloc[:,1],df_ans.iloc[:,0], 
                       facecolor='lightgray', 
                       alpha=0.25)


plt.plot(df_ans.iloc[:,5],'.b',label = 'min excess temperature for the year 2015')
plt.plot(df_ans.iloc[:,6],'.r',label = 'max excess temperature for the year 2015')

plt.legend()
plt.xlabel("month (the year reflects the comparison year 2015)",size = 12)
plt.ylabel("temperature (degrees C)",size = 13)
plt.title("Extreme temperatures reached throughout period 2005-2014, \n and excesses for the year 2015 over that period",size=16)

#remove frame
for spine in plt.gca().spines.values():
    spine.set_visible(False)
#remove ticks
plt.tick_params(top='off', bottom='off', left='on', right='off', labelleft='on', labelbottom='on')
plt.show()


plt.savefig('foo.pdf',bbox_inches='tight')
