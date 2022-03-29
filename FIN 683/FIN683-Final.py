# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 08:18:03 2021

@author: seph
"""

"""FIN 683 FINAL"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import scipy.optimize as optimize

### Final Exam with 4-Fund Portfolio Optimization ### 

# Question 7

Mkt_rets = 0.06
Mkt_sd = 0.16

A_rets = 0.12
A_beta = 1.5
A_fs_sd = 0.25

B_rets = 0.04
B_beta = 0.5
B_fs_sd = 0.20

C_rets = 0.08
C_beta = 1.25
C_fs_sd = 0.30

rf = 0.02

# 7.1 
A_rets_CAPM = rf + A_beta * (Mkt_rets - rf)
B_rets_CAPM = rf + B_beta * (Mkt_rets - rf)
C_rets_CAPM = rf + C_beta * (Mkt_rets - rf)

A_alpha = A_rets - A_rets_CAPM
B_alpha = B_rets - B_rets_CAPM
C_alpha = C_rets - C_rets_CAPM

print(f'Question 7.1:\n CAPM alpha of Stock A = {A_alpha}\n CAPM alpha of Stock B = {B_alpha}\n CAPM alpha of Stock C = {C_alpha}')

# 7.2 4-Fund Portfolio Optimization

def f_SI(params):
    A_w, B_w, C_w = params
    Market_w = (1 - (A_w + B_w + C_w))
    port_alpha = A_w*A_alpha + B_w*B_alpha + C_w*C_alpha#<-- Mkt alpha = 0
    port_beta = A_w*A_beta + B_w*B_beta + C_w*C_beta + Market_w*1 #<-- Mkt beta = 1
    port_rets = port_alpha + port_beta * (Mkt_rets - rf)
    port_var = ((port_beta ** 2)*(Mkt_sd**2)
                +(A_w**2)*(A_fs_sd**2)
                +(B_w**2)*(B_fs_sd**2)
                +(C_w**2)*(C_fs_sd**2)
                +(Market_w**2)*(0)) #<-- Market residual sd = 0
    return -(port_rets / (port_var**(1/2)))
                        
initial_guess = [1, 1, 1]
result = optimize.minimize(f_SI, initial_guess)
if result.success:
    fitted_params = result.x
    print(f'\nQuestion 7.2 Single Index Model Results:\nSharpe Ratio = {-f_SI(fitted_params)}')
    fitted_params = np.append(fitted_params,[(1-fitted_params.sum())])
    df_ORP_SingleIndex = pd.DataFrame(fitted_params, 
                          index = ['Stock_A', 'Stock_B', 'Stock_C', 'Market'],
                          columns = ['Weights'])
    print('  Weights:')
    print(f'    Stock A = {df_ORP_SingleIndex.Weights[0]}')
    print(f'    Stock B = {df_ORP_SingleIndex.Weights[1]}')
    print(f'    Stock C = {df_ORP_SingleIndex.Weights[2]}')
    print(f'    Market = {df_ORP_SingleIndex.Weights[3]}')
    print('  Portfolio Beta = 1.28629218066804') #<-- Estimate from printing port_beta final result in f_SI function.
else:
    raise ValueError(result.message)
    
# 7.3 
print('\nQuestion 7.3 How to change(improve) the Sharpe Ratio of a Portfolio without adjusting beta:')
print(' 1. Find more alpha (difficult to do).')
print(' 2. Decrease the Sharpe Ratio denominator by decreasing portfolio variance i.e. more diversification (weights are squared so denominator will decrease with more stocks).')

# Question 8

df_Q8 = pd.read_csv('final_file_python.csv')
df_Q8.rename(columns = {df_Q8.columns[0]: 'Date'},
                    inplace = True)
df_Q8['Date'] = pd.to_datetime(df_Q8['Date'], format='%Y%m')
df_Q8 = df_Q8.set_index('Date')
df_Q8 = df_Q8 / 100

# Single (CAPM) Regression

Hedge_fitted = smf.ols("Hedge_Excess_return ~ MKT_RF", df_Q8).fit()
print('\nQuestion 8.1 Single (CAPM) Regression Results:')
print(Hedge_fitted.summary())

# Multiple (FF) Regression

Hedge_multiple_fitted = smf.ols("Hedge_Excess_return ~ MKT_RF + SMB + HML + RF", df_Q8).fit()
print('\nQuestion 8.2 Multiple (F-F 3-Factor) Regression Results:')
print(Hedge_multiple_fitted.summary())
print('\nQuestion 8.3 When might an investor be interested in this hedge fund strategy?')
print('\nRegression of the hedge fund excess returns against the market shows that the fund is not performing better than the market with an alpha equal to 0 (statistically insignificant with p-value of 0.378).')
print(f"\nHowever, the multiple regression with the F-F 3 factors results in an annual alpha of {Hedge_multiple_fitted.params.Intercept * 12}. This means that the fund's performance cannot be explained by the 3 Factor Model." )
print("\nTherefore, although the fund's overall alpha when regressing against the CAPM is 0, they are employing a strategy that cannot be explained by something as simple as the 3 Factor Model (inclusion of these factors results in a positive alpha). Their strategy therefore may have value in its novelty, and since past performance is not indicative of future performance, then there may be instances in the future when their unique strategy outperforms the market.")
print('\nAn investor paying a premium for this fund may be deterred however, since there has been no alpha to show for it when looking at the past 80+ years as a whole.')