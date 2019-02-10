# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 19:59:46 2019

@author: 121b2
"""
import pandas as pd
import wrds
# plotting in separate window
%matplotlib qt 
# back to normal
%matplotlib inline 

dfEcon = db.raw_sql('SELECT * FROM execcomp.anncomp')

dfEcon.info()
dfEcon.head()
dfEcon.to_csv('execComp.csv')




dfEcon = pd.read_csv('execComp.csv')

##############
dfEcon.loc[dfEcon['tdc1'].idxmax(),'tdc1']=dfEcon.loc[dfEcon['tdc1'].idxmax(),'tdc1']/1000
dfEcon.loc[dfEcon['tdc1'].idxmax(),'tdc1']=dfEcon.loc[dfEcon['tdc1'].idxmax(),'tdc1']/100
dfEcon['tdc1'].sort_values(ascending = False)[:5]
dfEcon.loc[dfEcon['tdc2'].idxmax(),'tdc2']=dfEcon.loc[dfEcon['tdc2'].idxmax(),'tdc2']/1000
dfEcon.loc[dfEcon['tdc2'].idxmax(),'tdc2']=dfEcon.loc[dfEcon['tdc2'].idxmax(),'tdc2']/100
dfEcon.loc[dfEcon['salary'].idxmax(),'salary']=dfEcon.loc[dfEcon['salary'].idxmax(),'salary']/1000
dfEcon.loc[dfEcon['salary'].idxmax(),'salary']=dfEcon.loc[dfEcon['salary'].idxmax(),'salary']/100

##################



db = wrds.Connection(wrds_username ='tycho1')

dfSp500 =db.raw_sql('SELECT * FROM crspa.msp500')
dfSp500.to_csv('sp500.csv')

dfSp500 = pd.read_csv('sp500.csv')

dfSp500['caldt'] = pd.to_datetime(dfSp500['caldt'])
dfSp500['month'] = pd.DatetimeIndex(dfSp500.iloc[:,0]).month
dfSp500['year'] = dfSp500['caldt'].apply(lambda x:x.year)
dfSp500y = dfSp500[dfSp500['month'] == 12]


dfSp500y = dfSp500y.set_index('year')
dfSp500y[['usdval']].plot()

dfSp500y[['spindx']].plot()

#sp = (dfSp500y[dfSp500y.index> pd.to_datetime('1991-10-01')][['spindx']])

sp = (dfSp500y[dfSp500y.index> 1991][['spindx']])
#sp.plot()
################



ax  = dfEcon.groupby(by=['year']).mean()[['tdc1',
                    'tdc2',
                    'salary',
                    'opt_unex_exer_num',
                    'option_awards_fv',
                    'othann','opt_exer_val',
                    'defer_balance_tot',
                    'bonus']].plot(lw=5)
ax.set_ylim(1,5000)
ax.axvspan(2000,2003,alpha=.3,color='red')
ax.axvspan(2008,2010,alpha=.2,color='green')
ax.yaxis.grid()

#options
ax  = dfEcon.groupby(by=['year']).mean()[['tdc1',
                     'salary',
                     'bonus',
                    'opt_unex_exer_est_val',
                    'opt_unex_unexer_est_val',
                    
                   
                    'option_awards_fv',
                    'opt_exer_val'
                    ]].plot(linewidth=2,style='-')
ax.set_ylim(1,5000)
ax.axvspan(2000,2003,alpha=.3,color='pink')
ax.axvspan(2008,2010,alpha=.2,color='lightgreen')

#stocks
ax  = dfEcon.groupby(by=['year']).mean()[['tdc1',
                     'stock_awards_fv',
                     'stock_awards',
                    'stock_unvest_val',
                    'shrs_vest_val',
                    'salary',
                    'bonus']].plot(linewidth=2,style='-')
ax.set_ylim(1,5000)
ax.axvspan(2000,2003,alpha=.3,color='pink')
ax.axvspan(2008,2010,alpha=.2,color='lightgreen')

#final
ax  = dfEcon.groupby(by=['year']).mean()[['tdc1',
                     'salary',
                     'bonus',
                     'opt_unex_exer_est_val',
                     'stock_unvest_val',

                   
                    'opt_exer_val'
                    ]].plot(linewidth=2,style='-')
ax.set_ylim(1,5000)
ax.axvspan(2000,2002,alpha=.3,color='pink')
ax.axvspan(2008,2010,alpha=.2,color='lightgreen')




##### for the final graph
import matplotlib.pyplot as plt
import numpy as np

dfPlot = dfEcon.groupby(by=['year']).mean()[['tdc1',
                     'salary',
                     'bonus',
                     'opt_unex_exer_est_val',
                     'stock_unvest_val',                  
                     'opt_exer_val']]

dfPlot.to_csv("execCompAggregated.csv")
numExec = len(set(dfEcon['exec_fullname']))#number of unique exec
numCorp = len(set(dfEcon['gvkey']))#number of unique companies


fig, ax = plt.subplots()
linewidth=[4,4,4,.51,.51,.51]
colours = ['darkblue','orange','g','blue','purple','gray']
for var,lw,last_value,colour in zip(dfPlot.columns,linewidth,dfPlot.values[dfPlot.shape[0]-1],colours):
    dfPlot[var].plot(lw=lw,ax=ax,color=colour)
    ax.text(2018.2,last_value,var,color = colour,size = 14)

ax.set_ylim(1,5000)
ax.set_xlim(1992,2020)
ax.axvspan(2000,2003,alpha=.3,color='pink')
ax.axvspan(2008,2010,alpha=.2,color='lightgreen')
ax.yaxis.grid(color='grey', linestyle='--', linewidth=.2)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.xaxis.set_ticks(np.arange(1992, 2018, 2))
ax.text(1992, 4500, ' Number of unique executives:  {:.0f} \n Number of unique companies:  {:.0f}'.format(numExec,numCorp), style='italic',
        bbox={'facecolor':'lightblue', 'alpha':0.2, 'pad':10})
ax.text(1992, 1500, ' Source: Compustad / WRDS', style='italic',
        bbox={'facecolor':'lightblue', 'alpha':0.05, 'pad':3},size=8)



#ax.legend(loc='left')
ax.set_ylabel('Average annual compensation in thousands of dollars', color='darkblue',size=16)
ax.tick_params('y', colors='darkblue')
######
ax2 = ax.twinx()
sp.plot(ax=ax2,lw=4,color='r')
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_visible(False)

ax2.get_legend().remove()
ax2.text(2018.2,sp.iloc[len(sp)-1,0],'sp500',color = 'r',size = 12)

ax2.legend().set_visible(False)
ax2.set_ylabel('Value of the index S&P500', color='r',size = 16)
ax2.tick_params('y', colors='r')




