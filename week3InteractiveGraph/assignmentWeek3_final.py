# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 11:55:49 2019

@author: 121b2
"""

# Use the following data for this assignment:
#%matplotlib qt 


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])
#df
#help(plt.bar)

x = df.mean(axis=1)
ster = (df.std(axis=1)/df.shape[1]**.5)*1.96 # standard error


##animation
import matplotlib.animation as animation
# for the animation


###interactive plotting 
plt.figure()
error_config = {'ecolor': '0.4'}
plt.bar(list(map(str,x.index)),x,yerr = list(ster),error_kw=error_config,capsize=10,color='lightblue')

def onclick(event):
    plt.cla()
    bars = plt.bar(list(map(str,x.index)),x,yerr = list(ster),
                   edgecolor='black',width = 1.0,
                   error_kw=error_config,capsize=10,color='lightblue')
    y_val = round(event.ydata)
    plt.axhline(y=y_val, color='g')
    plt.gca().set_title('You have chosen the value of: {:.0f}'.format(y_val))#(event.ydata))
    #
    for i,bar in enumerate(bars): #print(bar,i)
        if y_val == round(bar.get_height()):
            bar.set_color('white')
        elif y_val > bar.get_height() + ster[i+1992]:
            bar.set_color('darkblue')
        elif y_val < bar.get_height() - ster[i+1992]:
            bar.set_color('darkred')
        
  
plt.gcf().canvas.mpl_connect('button_press_event', onclick)


