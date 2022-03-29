# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 10:14:44 2021

@author: seph
"""

### Analysis of Fama/French Factors and ETF Strategy ###

import pandas as pd
import statsmodels.formula.api as smf

# 1. CAPM Regression of Fama/French Factors

df_3F = pd.read_csv('F-F_Research_Data_Factors_daily.csv')
df_3F.rename(columns = {df_3F.columns[0]: 'Date'},
                    inplace = True)
df_3F['Date'] = pd.to_datetime(df_3F['Date'], format='%Y%m%d')
df_3F = df_3F.set_index('Date')
df_3F = df_3F / 100
df_3F = df_3F.rename(columns = {'Mkt-RF' : 'Mkt'})

df_MOM = pd.read_csv('F-F_Momentum_Factor_daily.csv') 
df_MOM.rename(columns = {df_MOM.columns[0]: 'Date'},
                    inplace = True)
df_MOM['Date'] = pd.to_datetime(df_MOM['Date'], format='%Y%m%d')
df_MOM = df_MOM.set_index('Date')
df_MOM = df_MOM / 100

df_3F['MOM'] = df_MOM['Mom']
df_3F = df_3F.loc["1926-11-03":]

df_ETF = pd.read_csv('ETF_returns_683_students.csv')
df_ETF.rename(columns = {df_ETF.columns[0]: 'Date'},
                    inplace = True)
df_ETF['Date'] = pd.to_datetime(df_ETF['Date'], format='%Y%m%d')
df_ETF = df_ETF.set_index('Date')

df_1A = df_3F.loc[:"2000-1-01"]
df_1B = df_3F.loc["2000-01-01":]
df_1C = df_3F.copy()

# Question 1A:
HML_fitted1A = smf.ols("HML ~ Mkt", df_1A).fit()
SMB_fitted1A = smf.ols("SMB ~ Mkt", df_1A).fit()

print(SMB_fitted1A.summary())
MOM_fitted1A = smf.ols("MOM ~ Mkt", df_1A).fit()

print('Question 1A (1926 to 2000):')
print(f' HML alpha = {HML_fitted1A.params.Intercept:{.4}}, p = {HML_fitted1A.pvalues.Intercept:{.4}} | HML beta = {HML_fitted1A.params.Mkt:{.4}}, p = {HML_fitted1A.pvalues.Mkt:{.4}}' )
print(f' SMB alpha = {SMB_fitted1A.params.Intercept:{.4}}, p = {SMB_fitted1A.pvalues.Intercept:{.4}} | SMB beta = {SMB_fitted1A.params.Mkt:{.4}}, p = {SMB_fitted1A.pvalues.Mkt:{.4}}' )
print(f' MOM alpha = {MOM_fitted1A.params.Intercept:{.4}}, p = {MOM_fitted1A.pvalues.Intercept:{.4}} | MOM beta = {MOM_fitted1A.params.Mkt:{.4}}, p = {MOM_fitted1A.pvalues.Mkt:{.4}}\n' )

#Question 1B:
HML_fitted1B = smf.ols("HML ~ Mkt", df_1B).fit()
SMB_fitted1B = smf.ols("SMB ~ Mkt", df_1B).fit()
MOM_fitted1B = smf.ols("MOM ~ Mkt", df_1B).fit()  

print('Question 1B (2000 to 2021):')
print(f' HML alpha = {HML_fitted1B.params.Intercept:{.4}}, p = {HML_fitted1B.pvalues.Intercept:{.4}} | HML beta = {HML_fitted1B.params.Mkt:{.4}}, p = {HML_fitted1B.pvalues.Mkt:{.4}}' )
print(f' SMB alpha = {SMB_fitted1B.params.Intercept:{.4}}, p = {SMB_fitted1B.pvalues.Intercept:{.4}} | SMB beta = {SMB_fitted1B.params.Mkt:{.4}}, p = {SMB_fitted1B.pvalues.Mkt:{.4}}' )
print(f' MOM alpha = {MOM_fitted1B.params.Intercept:{.4}}, p = {MOM_fitted1B.pvalues.Intercept:{.4}} | MOM beta = {MOM_fitted1B.params.Mkt:{.4}}, p = {MOM_fitted1B.pvalues.Mkt:{.4}}\n' )

#Question 1C:
HML_fitted1C = smf.ols("HML ~ Mkt", df_1C).fit()
SMB_fitted1C = smf.ols("SMB ~ Mkt", df_1C).fit()
MOM_fitted1C = smf.ols("MOM ~ Mkt", df_1C).fit()  

print('Question 1C (1926 to 2021):')
print(f' HML alpha = {HML_fitted1C.params.Intercept:{.4}}, p = {HML_fitted1C.pvalues.Intercept:{.4}} | HML beta = {HML_fitted1C.params.Mkt:{.4}}, p = {HML_fitted1C.pvalues.Mkt:{.4}}' )
print(f' SMB alpha = {SMB_fitted1C.params.Intercept:{.4}}, p = {SMB_fitted1C.pvalues.Intercept:{.4}} | SMB beta = {SMB_fitted1C.params.Mkt:{.4}}, p = {SMB_fitted1C.pvalues.Mkt:{.4}}' )
print(f' MOM alpha = {MOM_fitted1C.params.Intercept:{.4}}, p = {MOM_fitted1C.pvalues.Intercept:{.4}} | MOM beta = {MOM_fitted1C.params.Mkt:{.4}}, p = {MOM_fitted1C.pvalues.Mkt:{.4}}\n' )

# 2. Regression of given ETF against Market and Fama/French Factors to determine ETF Strategy employed

df_2 = df_ETF['Group 5'].copy().to_frame()
df_2 = df_2.rename(columns = {'Group 5' : 'ETF'})
"""Assuming Group 5 ETF"""

df_2['Mkt'] = df_3F['Mkt']
df_2['SMB'] = df_3F['SMB']
df_2['HML'] = df_3F['HML']
df_2['MOM'] = df_3F['MOM']

ETF_fitted2A = smf.ols("ETF ~ Mkt", df_2).fit()
ETF_fitted2B = smf.ols("ETF ~ SMB + HML + MOM + Mkt", df_2).fit()

print(ETF_fitted2A.summary())
print(ETF_fitted2B.summary())
print(ETF_fitted2B.params.Intercept * (252))




