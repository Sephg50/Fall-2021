# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 17:39:12 2021

@author: sepeh
"""

from math import sqrt, exp
import pandas as pd
import numpy as np


### Option Pricing with Monte Carlo Simulation ###

S = 310
K = 300
r = 0.03
"""r = DOMESTIC exchange rate"""
q = 0
""" q = 0 if no dividend given, q = FOREIGN exchange rate """
sigma = 0.5 
T = 1
trials = 1000

def stock_price(S,r,q,sigma, T):
    return(S*exp(((r-q)-0.5*(sigma**2))*T+sigma*sqrt(T)*np.random.normal(0,1)))

d = []
for i in range(0,trials):
    d.append(stock_price(S,r,q,sigma,T))
    
df = pd.DataFrame(d)
    
call = []
put = []
for stock in df[0]:
    call.append(max(0,stock-K))
    put.append(max(0, K-stock))

df['call'] = call  
df['put'] = put
df = df.rename(columns = {df.columns[0] : 'spot'})

call_price = df['call'].mean()*exp(-r*T)
put_price = df['put'].mean()*exp(-r*T)

print(f'Monte Carlo Simulation with {trials} trials: \n Spot Price = {S} \n Strike Price = {K} \n T = {T} \n r = {r} \n Dividend = {q} \n sigma = {sigma} \n ---------------')
print(f'call price = {call_price}')
print(f'put price = {put_price}')