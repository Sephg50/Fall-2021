#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 08:12:11 2021

@author: seph
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import scipy.optimize as optimize


### Three-Fund Portfolio Optimization (Markowitz Model and Single Index Model) ###

# Part 1: Analyze PFE and ABBV historical stock prices

ff = pd.read_csv('F-F_Research_Data_Factors.csv',
                 parse_dates = True,
                 index_col = 'Date')
ff= ff / 100

stocks = pd.read_csv('PFE_ABBV.csv', parse_dates = True, index_col = 'Date')
stocks['PFE rets'] = stocks['PFE Adj Close'].pct_change()
stocks['ABBV rets'] = stocks['ABBV Adj Close'].pct_change()
stocks.drop(stocks.head(1).index,inplace = True)

portfolio = pd.DataFrame(index = stocks.index)
portfolio['PFE'] = stocks['PFE rets'] - ff['RF']
portfolio['ABBV'] = stocks['ABBV rets'] - ff['RF']
portfolio['Market'] = ff['Mkt-RF']

PFE_avg = portfolio['PFE'].mean() * 12
ABBV_avg = portfolio['ABBV'].mean() * 12
Market_avg = portfolio['Market'].mean() * 12

PFE_std = portfolio['PFE'].std() * (12**(1/2))
ABBV_std = portfolio['ABBV'].std() * (12**(1/2))
Market_std = portfolio['Market'].std() * (12**(1/2))

d = {'Average Rets' : [PFE_avg, ABBV_avg, Market_avg],
     'Std Dev' : [PFE_std, ABBV_std, Market_std]}

annual_df = pd.DataFrame(d,
                         index = ['PFE',
                                  'ABBV',
                                  'Market'])

corr = portfolio.corr()
PFE_ABBV_corr = corr.loc['PFE', 'ABBV']
PFE_market_corr = corr.loc['PFE', 'Market']
ABBV_market_corr = corr.loc['ABBV', 'Market']
    
PFE_fitted = smf.ols('PFE ~ Market', portfolio).fit()
print(PFE_fitted.summary())

p = PFE_fitted.params
ax = np.arange(-2,2)
PFE_fitted_plot = portfolio.plot.scatter(x = 'Market',
                                    y = 'PFE')
PFE_fitted_plot.plot(ax, p.Intercept + p.Market * ax)
PFE_fitted_plot.set_xlim([-0.2,0.2])
PFE_fitted_plot.set_ylim([-0.2,0.3])
PFE_fitted_plot.text(-0.15, 0.2, f'{p.Market:{.4}}x + {p.Intercept:{.4}}')
PFE_fitted_plot.text(-0.15, 0.15, f'R squared = {PFE_fitted.rsquared:{.4}}')
PFE_fitted_plot.set_title('Monthly PFE Excess Returns versus Monthly Market Excess Returns')

ABBV_fitted = smf.ols('ABBV ~ Market', portfolio).fit()
print(ABBV_fitted.summary())

p = ABBV_fitted.params
ax = np.arange(-2,2)
ABBV_fitted_plot = portfolio.plot.scatter(x = 'Market',
                                    y = 'ABBV')
ABBV_fitted_plot.plot(ax, p.Intercept + p.Market * ax)
ABBV_fitted_plot.set_xlim([-0.2,0.2])
ABBV_fitted_plot.set_ylim([-0.3,0.3])
ABBV_fitted_plot.text(-0.15, 0.2, f'{p.Market:{.4}}x + {p.Intercept:{.4}}')
ABBV_fitted_plot.text(-0.15, 0.15, f'R squared = {ABBV_fitted.rsquared:{.4}}')
ABBV_fitted_plot.set_title('Monthly ABBV Excess Returns versus Monthly Market Excess Returns')

PFE_residual_std = PFE_fitted.resid.std() * (12**(1/2))
ABBV_residual_std = ABBV_fitted.resid.std() * (12**(1/2))

d2 = {'Alpha' : [PFE_fitted.params.Intercept, ABBV_fitted.params.Intercept],
      'Beta' : [PFE_fitted.params.Market, ABBV_fitted.params.Market]}

alpha_beta_df = pd.DataFrame(d2,
                             index = ['PFE', 'ABBV'])

# Part 2: Construct Optimal Risky Portfolios

alpha = 0.01
market_expected = 0.06
PFE_expected = alpha + PFE_fitted.params.Market * market_expected
ABBV_expected = alpha + ABBV_fitted.params.Market * market_expected

"""
expected portfolio return = w1 * PFE_expected + w2 * ABBV_expected + w3 * market_expected

portfolio variance = (((w1 ** 2) * (PFE_std ** 2)
                      + (w2 ** 2) * (ABBV_std ** 2)
                      + (w3 ** 2) * (Market_std ** 2)) + (
                          2 * w1 * w2 * PFE_ABBV_corr * PFE_std * ABBV_std)
                          + (2 * w1 * w3 * PFE_market_corr * PFE_std * Market_std)
                          + (2 * w2 * w3 * ABBV_market_corr * ABBV_std * Market_std))
                          
Sharpe Ratio = expected portfolio return / portfolio sd

solve for w1, w2, w3 such that SR is maximized
"""

def f(params):
    PFE_w, ABBV_w = params
    Market_w = (1 - (PFE_w + ABBV_w))
    port_var = (((PFE_w ** 2) * (PFE_std ** 2)
                      + (ABBV_w ** 2) * (ABBV_std ** 2)
                      + (Market_w ** 2) * (Market_std ** 2)) + (
                          2 * PFE_w * ABBV_w * PFE_ABBV_corr * PFE_std * ABBV_std)
                          + (2 * PFE_w * Market_w * PFE_market_corr * PFE_std * Market_std)
                          + (2 * ABBV_w * Market_w * ABBV_market_corr * ABBV_std * Market_std))
    port_rets = (PFE_w * PFE_expected + ABBV_w * ABBV_expected + Market_w * market_expected)
    return -(port_rets / (port_var**(1/2)))
                        
initial_guess = [1, 1]
result = optimize.minimize(f, initial_guess)
if result.success:
    fitted_params = result.x
    print(f'Markowitz Model Results: \nSharpe Ratio = {-f(fitted_params)}')
    fitted_params = np.append(fitted_params,[(1-fitted_params.sum())])
    print(fitted_params)
    df_ORP_Markowitz = pd.DataFrame(fitted_params, 
                          index = ['PFE', 'ABBV', 'Market'],
                          columns = ['Weights'])
else:
    raise ValueError(result.message)
    
"""
Single Index Model:
    expected portfolio rets = port alpha + port beta * E[R]Mkt
    port alpha = w1*alpha1 + w2*alpha2 + w3*alpha3
    port beta = w1*beta1 + w2*beta2 + w3*beta3
    portfolio sd = sqrt((port beta ** 2)*(sd market **2)
                        +(w1**2)*(sd residual 1**2)
                        +(w2**2)*(sd residual 2**2)
                        +(w3**2)*(sd residual 3**2))
"""
alpha_PFE = 0.01
alpha_ABBV = 0.01

def f_SI(params):
    PFE_w, ABBV_w = params
    Market_w = (1 - (PFE_w + ABBV_w))
    port_alpha = PFE_w*alpha_PFE + ABBV_w*alpha_ABBV #<-- Mkt alpha = 0
    port_beta = PFE_w*PFE_fitted.params.Market + ABBV_w*ABBV_fitted.params.Market + Market_w*1 #<-- Mkt beta = 1
    port_rets = port_alpha + port_beta * market_expected
    port_var = ((port_beta ** 2)*(Market_std**2)
                +(PFE_w**2)*(PFE_residual_std**2)
                +(ABBV_w**2)*(ABBV_residual_std**2)
                +(Market_w**2)*(0)) #<-- Market residual sd = 0
    return -(port_rets / (port_var**(1/2)))
                        
initial_guess = [1, 1]
result = optimize.minimize(f_SI, initial_guess)
if result.success:
    fitted_params = result.x
    print(f'\nSingle Index Model Results:\nSharpe Ratio = {-f_SI(fitted_params)}')
    fitted_params = np.append(fitted_params,[(1-fitted_params.sum())])
    print(fitted_params)
    df_ORP_SingleIndex = pd.DataFrame(fitted_params, 
                          index = ['PFE', 'ABBV', 'Market'],
                          columns = ['Weights'])
else:
    raise ValueError(result.message)
    
    

