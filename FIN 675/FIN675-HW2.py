# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 14:59:14 2021

@author: seph
"""

### Analysis of U.S. Treasury Bond Modified Duration and Convexity ###

import pandas as pd
from sympy.solvers import solve
from sympy import Symbol
import numpy_financial as npf

# 1. Calculation of current par rate for 30-year treasury bonds and 100-year treasury bonds
yields = pd.read_csv('fin675_hwk2.csv', 
                     index_col = 'Years to Maturity')
yields = yields.loc[:, ~yields.columns.str.contains('^Unnamed')]
yields.plot()

current_yields = yields.loc[:,'Current Yield Curve']
current_yields = current_yields.to_frame().rename(columns = {'Current Yield Curve':'Yield'})
current_yields.index.names = ['Maturity']

current_yields = current_yields.loc[:,:] / 100

current_yields['DF'] = 1 / ((1 + (current_yields['Yield']))**current_yields.index.values)
current_yields['cDF'] = current_yields['DF'].cumsum()

x = Symbol('x')
par = []
for df, cdf in zip(current_yields['DF'], current_yields['cDF']):
      par += solve((((x*100*cdf+100*df-100))))
current_yields['Par'] = [float(x) for x in par]

# 2. Plotting bond price and yield for 30-year and 100-year treasury bonds
yield_index = [i/2 for i in range(2,21)]

price_to_yield = pd.DataFrame(index = yield_index)
price_to_yield.index.names = ['Yield %']

price_to_yield['30yr Price'] = -npf.pv(price_to_yield.index.values/100, 
                                        30, 
                                        current_yields.loc[30, 'Par']*100) + (100/((1 + (price_to_yield.index.values/100))**30))
price_to_yield['100yr Price'] = -npf.pv(price_to_yield.index.values/100, 
                                        100, 
                                        current_yields.loc[100, 'Par']*100) + (100/((1 + (price_to_yield.index.values/100))**100))

py_curve = price_to_yield.plot()
py_curve.set_ylabel('Price')
py_curve.set_title('Price-to-Yield')

# 3. Modified Duration and Convexity calculations

yr30 = pd.DataFrame(index = current_yields.index[0:30])
yr30['CF'] = current_yields.loc[30, 'Par']*100
yr30.loc[30,'CF'] += 100 
yr30['PV'] = yr30['CF'] / ((1 + current_yields.loc[30, 'Par'])**yr30.index.values)
yr30['Weight'] = yr30['PV'] / yr30['PV'].sum()
yr30['D Mac'] = yr30.index.values 
yr30['Convexity'] = yr30['D Mac']**2

yr100 = pd.DataFrame(index = current_yields.index)
yr100['CF'] = current_yields.loc[100, 'Par']*100
yr100.loc[100,'CF'] += 100 
yr100['PV'] = yr100['CF'] / ((1 + current_yields.loc[100, 'Par'])**yr100.index.values)
yr100['Weight'] = yr100['PV'] / yr100['PV'].sum()
yr100['D Mac'] = yr100.index.values 
yr100['Convexity'] = yr100['D Mac']**2

yr30_dmac = (yr30['D Mac'] * yr30['Weight']).sum()
yr30_dmod = yr30_dmac / (1 + current_yields.loc[30, 'Par'])
yr30_convexity = (yr30['Convexity'] * yr30['Weight']).sum()

yr100_dmac = (yr100['D Mac'] * yr100['Weight']).sum()
yr100_dmod = yr100_dmac / (1 + current_yields.loc[100, 'Par'])
yr100_convexity = (yr100['Convexity'] * yr100['Weight']).sum()

price_to_yield['30yr D'] = 100 * (1 + yr30_dmod * (current_yields.loc[30, 'Par'] - price_to_yield.index.values/100))
price_to_yield['30yr D+C'] = price_to_yield['30yr D'] + 0.5 * (
    current_yields.loc[30, 'Par'] - price_to_yield.index.values/100) ** 2 * 100 * yr30_convexity
price_to_yield['100yr D'] = 100 * (1 + yr100_dmod * (current_yields.loc[100, 'Par'] - price_to_yield.index.values/100))
price_to_yield['100yr D+C'] = price_to_yield['100yr D'] + 0.5 * (
    current_yields.loc[100, 'Par'] - price_to_yield.index.values/100) ** 2 * 100 * yr100_convexity

yr30_curve = price_to_yield.plot(y = ['30yr Price', '30yr D', '30yr D+C'])
yr30_curve.set_ylim([0,175])
yr30_curve.set_ylabel('Price')
yr30_curve.set_title('30 Year Bond Price-to-Yield with Duration and Convexity')
                                                          
yr100_curve = price_to_yield.plot(y = ['100yr Price', '100yr D', '100yr D+C'])
yr100_curve.set_ylim([0,250])
yr100_curve.set_ylabel('Price')
yr100_curve.set_title('100 Year Bond Price-to-Yield with Duration and Convexity')

# 4. Analysis of 1% YTM increase on Modified Duration, Convexity, Bond Price
new_price30yr = -npf.pv(current_yields.loc[30, 'Par']+0.01,
                    30,
                    current_yields.loc[30, 'Par']*100) + (100/((1 + current_yields.loc[30, 'Par'] + 0.01))**30)
new_price30yr_d = 100 * (1 + yr30_dmod * (current_yields.loc[30, 'Par'] - (current_yields.loc[30, 'Par'] + 0.01)))
new_price30yr_dc = new_price30yr_d + 0.5 * (
    current_yields.loc[30, 'Par'] - (current_yields.loc[30, 'Par'] + 0.01)) ** 2 * 100 * yr30_convexity

new_price30yr_change_d = abs(new_price30yr - new_price30yr_d)
new_price30yr_change_dc = abs(new_price30yr - new_price30yr_dc)

price_to_yield['30yr D difference'] = abs(price_to_yield['30yr Price'] - price_to_yield['30yr D'])
price_to_yield['30yr D+C difference'] = abs(price_to_yield['30yr Price'] - price_to_yield['30yr D+C'])
price_to_yield['100yr D difference'] = abs(price_to_yield['100yr Price'] - price_to_yield['100yr D'])
price_to_yield['100yr D+C difference'] = abs(price_to_yield['100yr Price'] - price_to_yield['100yr D+C'])

new_price100yr = -npf.pv(current_yields.loc[100, 'Par']+0.01,
                    100,
                    current_yields.loc[100, 'Par']*100) + (100/((1 + current_yields.loc[100, 'Par'] + 0.01))**100)
new_price100yr_d = 100 * (1 + yr100_dmod * (current_yields.loc[100, 'Par'] - (current_yields.loc[100, 'Par'] + 0.01)))
new_price100yr_dc = new_price100yr_d + 0.5 * (
    current_yields.loc[100, 'Par'] - (current_yields.loc[100, 'Par'] + 0.01)) ** 2 * 100 * yr100_convexity

new_price100yr_change_d = abs(new_price100yr - new_price100yr_d)
new_price100yr_change_dc = abs(new_price100yr - new_price100yr_dc)

new_price_df = pd.DataFrame(data = {'Duration Estimate Price Diff' : [new_price30yr_change_d, new_price100yr_change_d],
                                    'Duration+Convexity Estimate Price Diff' : [new_price30yr_change_dc, new_price100yr_change_dc]},
                                      index = ['30 year', '100 year'])
new_price_graph = new_price_df.plot.bar(rot=0)
new_price_graph.set_ylabel('Price Difference')
new_price_graph.set_title('Accuracy of Duration and Duration+Convexity Estimates with 1% Increase in YTM')
duration_accuracy = price_to_yield.plot(y = ['30yr D difference', '100yr D difference'])
duration_accuracy.set_title('Duration Accuracy for 30yr and 100yr Bonds')
duration_accuracy.set_ylabel('Absolute Price Difference')

yr30_accuracy = price_to_yield.plot(y = ['30yr D difference', '30yr D+C difference'])
yr30_accuracy.set_title('30yr Curve Accuracy')
yr30_accuracy.set_ylabel('Absolute Price Difference')
yr30_accuracy.set_ylim([0,40])

yr100_accuracy = price_to_yield.plot(y = ['100yr D difference', '100yr D+C difference'])
yr100_accuracy.set_title('100yr Curve Accuracy')
yr100_accuracy.set_ylabel('Absolute Price Difference')
yr100_accuracy.set_ylim([0,100])



