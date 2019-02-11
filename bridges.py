#!/usr/bin/env python3


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as clr

def get_lat(pds):
    a = pd.to_numeric(pds.str[:2])
    b = pd.to_numeric(pds.str[2:4])/60
    c = pd.to_numeric(pds.str[4:8])/(60*60*100)
    r = a+b+c
    return r

def get_long(pds):
    a = pd.to_numeric(pds.str[:3])
    b = pd.to_numeric(pds.str[3:5])/60
    c = pd.to_numeric(pds.str[5:9])/(60*60*100)
    return a+b+c
    

def bridges():
    fname = 'data/2017HwyBridgesDelimitedAllStates.txt'
    use_col = ['LAT_016', 'LONG_017','STATE_CODE_001', 'CAT10', 'YEAR_BUILT_027', 'STRUCTURE_NUMBER_008']
    dtype = {'LAT_016': str, 'LONG_017':str, 'STATE_CODE_001':int}
    df = pd.read_csv(fname, nrows=1000000, encoding='ISO-8859-1', usecols=use_col, dtype=dtype)
    print(df['STATE_CODE_001'].sample(10))
    a = df['LAT_016'].str[:2]

    df['lat'] = get_lat(df['LAT_016'])
    df['long']= get_long(df['LONG_017'])
    slct = (df['long'] < 130) & (df['long'] > 65) & (df['lat']>20) & (df['lat']<50)
    df = df[slct]
    df =df[(df['lat']!=0) & (df['long']!=0)]
    print(np.unique(df['CAT10']))
    cond = ['G', 'F', 'P', 'N']
    cond_labels = ['Good Condition', 'Fair Condition', 'Poor Condition', 'N']
    cond_colors = ['g','y','r', 'r']
    plt.figure()
    for i in range(0, 3):
        slct = df['CAT10']==cond[i]
        # plt.scatter(-df['long'][slct], df['lat'][slct], facecolors=cond_colors[i], alpha=0.01, edgecolors='none', label=cond_label[i])
        plt.plot(np.array(-df['long'][slct]), np.array(df['lat'][slct]), ','+cond_colors[i], alpha=0.03, label=None)
        plt.plot([],[],'.'+cond_colors[i], label=cond_labels[i])
    plt.legend(loc='best')
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.title("Bridges Tracked by Federal Highway Administration")
    plt.savefig('figs/map.png')

    
    h, xbins = np.histogram(df['YEAR_BUILT_027'],bins=np.arange(1890,2018))
    years = (xbins[1:]+xbins[:-1])/2.0
    plt.figure()
    plt.plot(years, h, 'k', label='All Bridges')
    for i in range(0,3):
        slct = df['CAT10']==cond[i]
        h, _ = np.histogram(df['YEAR_BUILT_027'][slct],bins=xbins)
        plt.plot(years, h, cond_colors[i], label=cond_labels[i])
    plt.legend(loc='best')
    plt.xlabel('Year Built')
    plt.ylabel('Counts')
    plt.savefig('figs/year_condition.png')

    
    h_tot, xbins = np.histogram(df['YEAR_BUILT_027'][df['CAT10']!='N'],bins=np.arange(1890,2018))
    years = (xbins[1:]+xbins[:-1])/2.0
    plt.figure()

    previous_start = np.zeros_like(h_tot)
    for i in range(0,3):
        slct = df['CAT10']==cond[i]
        h, _ = np.histogram(df['YEAR_BUILT_027'][slct],bins=xbins)
        b = h/h_tot
        plt.fill_between(years,previous_start*100.0,(previous_start+b)*100.0,  color=cond_colors[i], alpha=0.7,label=cond_labels[i])
        previous_start = previous_start+b
    plt.xlabel('Year Built')
    plt.ylabel('Population Percent')
    plt.legend(loc=4, framealpha=0.3)
    plt.ylim([0,100])
    plt.xlim([np.min(years), np.max(years)])
    plt.title("Highway Bridge Condition by Year Built")
    plt.savefig("figs/condition_by_year.png")
    
    h_tot, xbins = np.histogram(df['lat'],bins=100)
    years = (xbins[1:]+xbins[:-1])/2.0
    plt.figure()
    previous_start = np.zeros_like(h_tot)
    for i in range(0,3):
        slct = df['CAT10']==cond[i]
        h, _ = np.histogram(df['lat'][slct],bins=xbins)
        b = h/h_tot
        plt.fill_between(years,previous_start,previous_start+b,  color=cond_colors[i], alpha=0.7)
        previous_start = previous_start+b
    plt.xlabel('Lat')
    plt.ylabel('Population Portion')
    plt.savefig("figs/condition_by_latitude.png")
    
    plt.figure()
    for i in range(0,3):
        slct = df['CAT10']==cond[i]
   
        plt.plot(df['YEAR_BUILT_027'][slct]+np.random.rand(np.sum(slct)), df['lat'][slct], ',', color=cond_colors[i], label=cond_labels[i], alpha=0.3)
    plt.ylabel('Lat')
    plt.xlabel('Year Built')

    
    fname = 'data/slubkin_992016-20170113122943.txt'
    use_col = ['LAT_016', 'LONG_017','STATE_CODE_001', 'CAT10', 'YEAR_BUILT_027', 'STRUCTURE_NUMBER_008']
    dtype = {'LAT_016': str, 'LONG_017':str, 'STATE_CODE_001':int, 'CAT10':str, 'YEAR_BUILT_027':float}
    df2 = pd.read_csv(fname, nrows=1000000, encoding='ISO-8859-1', usecols=use_col, dtype=dtype)

    df3 = df2.merge(right=df, on='STRUCTURE_NUMBER_008', suffixes=('_2016', '_2017'))

    print(df3.keys())
    slct_diff = df3['CAT10_2017'] != df3['CAT10_2016']
    slct_worse = (df3['CAT10_2017'] == 'P') & (df3['CAT10_2016'] != 'P')
    print(np.sum(slct_diff))
    print(np.sum(slct_worse))
    plt.figure()
    plt.plot(-df3['long'][slct_worse], df3['lat'][slct_worse], '.', alpha=1.0)
    plt.ylabel('Lat')
    plt.xlabel('Long')
    plt.title("Highway Bridges that Deteriorated to Poor Condition") 
    plt.legend()
    plt.savefig("figs/became_poor.png")

    plt.figure()
    h,xbins= np.histogram(df3['lat'][~slct_worse], bins=np.linspace(25,50,64), density=True)
    bin_cen = (xbins[:-1]+xbins[1:])/2.0
    plt.plot(bin_cen, h,  label='Remained >=Fair')
    h,_= np.histogram(df3['lat'][slct_worse], bins=xbins, density=True)
    plt.plot(bin_cen, h, label='Became Poor')
    plt.axvline(np.average(df3['lat'][slct_worse]), ls='--',color='#ff7f0e')
    plt.axvline(np.average(df3['lat'][~slct_worse]),ls='--',color='#1f77b4')
    plt.plot([],[],'k--', label='Average')
    plt.ylabel('PDF')
    plt.xlabel('Latitude')
    plt.legend(loc='best', framealpha=0.0)
    plt.title("Bridges tracked by Federal Highway Admin.")
    plt.savefig("figs/became_poor_by_latitide.png")

    print(np.average(df3['lat'][slct_worse]))
    print('vs')
    print(np.average(df3['lat'][~slct_worse]))

    plt.show()
    
if __name__ == "__main__":
    bridges()


