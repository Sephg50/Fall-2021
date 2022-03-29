# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 10:17:45 2021

@author: seph
"""

### Analysis of historical U.S. Stock Market Returns ###

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

# 1. Cleaning and preparing dataframe of stock market returns

ff = pd.read_csv('F-F_Research_Data_Factors_daily.CSV',
                          parse_dates = True)
ff.rename(columns = {ff.columns[0]: "Date"},
                    inplace = True)
ff.drop(ff.tail(2).index,inplace = True)
ff['Date'] = pd.to_datetime(ff['Date'], format='%Y%m%d')
ff['Mkt-RF'] = ff['Mkt-RF'] / 100
ff = ff.set_index('Date')

# 2. Resampled into monthly data for analysis
monthly_ff = ff['Mkt-RF'].resample('M').agg(lambda x: (x + 1).prod() - 1)
monthly_ff = monthly_ff.to_frame().rename(columns = {'Mkt-RF' : 'Monthly_rets'})
monthly_ff['Monthly_vol'] = ff['Mkt-RF'].resample('M').std()

vol_plot = monthly_ff['Monthly_vol'].plot()
vol_plot.set_title('Monthly Volatility 1926-2021')
monthly_ff['Vol_change'] = monthly_ff['Monthly_vol'].pct_change()

monthly_fitted = smf.ols('Monthly_rets ~ Vol_change', monthly_ff).fit() 
print(monthly_fitted.summary())
mf_plot = monthly_ff.plot.scatter(x = 'Vol_change',
                                  y = 'Monthly_rets')
mf_plot.set_title('Monthly Change in Volatility versus Monthly Cumulative Returns')

# 4. Analysis of 10 year rolling periods

rolling_ff = ff['Mkt-RF'].rolling(window = 2500).agg(lambda x: (x + 1).prod() - 1)
rolling_ff = rolling_ff.to_frame().rename(columns = {'Mkt-RF' : 'Rolling_rets'})
rolling_ff['Rolling_vol'] = ff['Mkt-RF'].rolling(window = 2500).std()


tenyear_ff = rolling_ff.resample('Y').last()
tenyear_ff = tenyear_ff.loc['1938':'2021']
tenyear_plot = tenyear_ff.plot(secondary_y = ['Rolling_vol'])
tenyear_plot.set_title('10 Year Rolling Returns and 10 Year Rolling Volatility 1938-2021')

# 5. Comparison of ABT stock returns and market returns

abt = pd.read_csv('ABT.csv', 
                          parse_dates = True, index_col = 'Date').drop(
                              columns = ['Open',
                                          'Low',
                                          'High', 
                                          'Close',
                                          'Volume'])
abt['Rets'] = abt['Adj Close'].pct_change()
abt = abt.loc["1980-03-18":"2021-03-31"]
abt.loc[:, 'Mkt-RF'] = ff['Mkt-RF']["1980-03-18":"2021-03-31"]

abt_mkt = abt.resample('M')[['Rets','Mkt-RF']].corr().stack().drop_duplicates().to_frame()
abt_mkt = abt_mkt.rename(columns = {abt_mkt.columns[0] : 'Corr'})
abt_mkt = abt_mkt.drop(abt_mkt.index[0])

monthly_abt = monthly_ff['Monthly_vol']['1980-03-18':'2021-03-31'].to_frame()
monthly_abt['Monthly_corr'] = abt_mkt.values
abt_fitted = smf.ols('Monthly_corr ~ Monthly_vol', monthly_abt).fit()

p = abt_fitted.params
ax = np.arange(0,2)
abt_plot = monthly_abt.plot.scatter(x = 'Monthly_vol',
                                    y = 'Monthly_corr')
abt_plot.plot(ax, p.Intercept + p.Monthly_vol * ax)
abt_plot.set_xlim([0,0.06])
abt_plot.set_ylim([0,1])
abt_plot.text(0.04, 0.5, f'{p.Monthly_vol:{.4}}x + {p.Intercept:{.4}}')
abt_plot.text(0.038, 0.4, f'R squared = {abt_fitted.rsquared:{.4}}')
abt_plot.set_title('Monthly Market Volatility versus the Monthly Correlation between ABT Daily Returns and Daily Market Premium')

print(abt_fitted.summary())


