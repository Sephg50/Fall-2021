# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 08:21:00 2021

@author: seph
"""

### Yield Curve Calculation from US T-bill spot rate ###

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sympy.solvers import solve
from sympy import Symbol
import numpy_financial as npf
from scipy.optimize import fsolve

yields = pd.read_csv('HWK1_bond_yields.csv', 
                          parse_dates = True, 
                          index_col = 'Maturity Date').drop(
                              columns=['State', 'S&P Rating'])
                             
yields = yields.loc[:, ~yields.columns.str.contains('^Unnamed')]
yields_6mo = yields[yields.index.month.isin([2,8]) 
                    & yields.index.day.isin([15]) 
                    & yields.Description.str.contains("STRIPPED INT")]
yields_6mo = yields_6mo.loc["2022-02-15":"2050-08-15"]
yields_6mo.loc[:, 'Midpoint'] = (yields_6mo['Yield Bid'] + yields_6mo['Yield Ask']) / 2
yields_6mo['Maturity'] = (np.arange(len(yields_6mo)) + 1) / 2

yields_6mo.loc[:, 'Price'] = 100 / (1 + (yields_6mo['Midpoint']/100)/2)**(2*yields_6mo['Maturity'])

yields_6mo['DF'] = yields_6mo['Price'] / 100

yields_6mo['Spot'] = yields_6mo['Midpoint'] / 100
  

# Forward rate 
yields_6mo['Forward'] = (((1 + yields_6mo['Spot']/2)**(yields_6mo['Maturity']*2)) / 
                          ((1 + yields_6mo['Spot'].shift(1)/2)**(yields_6mo['Maturity'].shift(1)*2)) - 1) * 2
yields_6mo.at['2022-02-15', 'Forward'] = yields_6mo.iloc[0]['Spot']

# Par rate
x = Symbol('x')
yields_6mo['cDF']=yields_6mo['DF'].cumsum()
par = []
for df, cdf in zip(yields_6mo['DF'], yields_6mo['cDF']):
     par += solve((((x/2*100*cdf+100*df-100))))
yields_6mo['Par'] = [float(x) for x in par]

# Annuity rate
def func(y):
    return (((-npf.pv(y/2, maturity * 2, 1)) - cdf)**2)
    
annuity = []
for maturity, cdf in zip(yields_6mo['Maturity'], yields_6mo['cDF']):
    annuity.append(fsolve(func, 0.02))
    
yields_6mo['Annuity'] = [float(i) for i in annuity]

yields_curves = yields_6mo[['Spot', 'Forward', 'Par', 'Annuity']]
yields_curves.plot()

plt.ylabel('Rate')


