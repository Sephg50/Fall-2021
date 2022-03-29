#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 12:09:40 2021

@author: seph
"""

### European Put Option pricing with BSM Model, 3-step Binomial Tree, and Monte Carlo Simulation ###

import pandas as pd
import numpy as np
from math import log, sqrt, exp
from scipy.stats import norm

prices = pd.read_csv('gold_prices.csv', parse_dates = True,
                     index_col = 'observation_date')
prices = prices.rename(columns = {'GOLDAMGBD228NLBM' : 'Price'})
prices.index.names = ['Date']

S = prices['Price'].iloc[0]
T = 1/12
K = 1850
r = 0.025
q = -0.01
prices['ln'] = np.log(prices.Price / prices.Price.shift(-1))
sigma = prices['ln'].std() * (252 ** (1/2))
size = 100

print(f'Spot Price: {S} \nStrike Price: {K} \ncontinuously-compounded risk-free rate = {r} p.a.\ndividend yield = {q} p.a.\nstdev = {sigma} p.a. \nT = {T}')
print('----------------------------------------------------------------')

def d1(S,K,T,r,q,sigma):
    return(log(S/K)+((r-q)+sigma**2/2)*T)/(sigma*sqrt(T))
def d2(S,K,T,r,q,sigma):
    return d1(S,K,T,r,q,sigma)-sigma*sqrt(T)
def bs_call(S,K,T,r,q,sigma):
    return S*exp(-q*T)*norm.cdf(d1(S,K,T,r,q,sigma))-K*exp(-r*T)*norm.cdf(d2(S,K,T,r,q,sigma))
def bs_put(S,K,T,r,q,sigma):
    return K*exp(-r*T)-S*exp(-q*T)+bs_call(S,K,T,r,q,sigma)
print(f'Black-Scholes Model: \n European Put option price = {bs_put(S,K,T,r,q,sigma) * size}')

steps = 3

T = (1/12)/3

u = exp(sigma*sqrt(T))
d = 1/u

p = (exp((r-q)*T) - d)/(u-d)

Suuu = S * u ** 3
Suud = S * (u ** 2) * d
Sudu = S * u * d * u
Sudd = S * u * d ** 2
Sduu = S * d * u ** 2
Sdud = S * d * u * d
Sddu = S * (d ** 2) * u
Sddd = S * d ** 3

Fuuu_put = max(0, K - Suuu)
Fuud_put = max(0, K - Suud)
Fudu_put = max(0, K - Sudu)
Fudd_put = max(0, K - Sudd)
Fduu_put = max(0, K - Sduu)
Fdud_put = max(0, K - Sdud)
Fddu_put = max(0, K - Sddu)
Fddd_put = max(0, K - Sddd)    

Fuu_put = (p * Fuuu_put + (1-p) * Fuud_put) * exp(-r*T)
Fud_put = (p * Fudu_put + (1-p) * Fudd_put) * exp(-r*T)
Fdu_put = (p * Fduu_put + (1-p) * Fdud_put) * exp(-r*T)
Fdd_put = (p * Fddu_put + (1-p) * Fddd_put) * exp(-r*T)

Fu_put = (p * Fuu_put + (1-p) * Fud_put) * exp(-r*T)
Fd_put = (p * Fdu_put + (1-p) * Fdd_put) * exp(-r*T)


F_put = (p * Fu_put + (1-p) * Fd_put) * exp(-r * T)

print(f'\nBinomial tree with {steps} steps: \n European Put option price = {F_put * size}')

trials = 1000
T = 1/12

def growth(r,q,sigma,T):
    return exp(((r-q)-0.5*(sigma**2))*T+sigma*sqrt(T)*np.random.normal(0,1))

d = []
g_avg = []
for i in range(0,trials):
    d.append(S * growth(r,q,sigma,T))
    g_avg.append(growth(r,q,sigma,T))
    
df = pd.DataFrame(d)
    
put = []
for stock in df[0]:
    put.append(max(0, K-stock))
    
df['put'] = put
df = df.rename(columns = {df.columns[0] : 'spot'})

put_price = df['put'].mean()*exp(-r*T)
se = df['put'].std() / sqrt(trials)

print(f'\nMonte Carlo Simulation with {trials} trials:')
print(f' European Put option price = {put_price * size} \n  95% Confidence Interval: [{(put_price - 1.965*se)*size}, {(put_price + 1.965*se)*size}]')

d_asian = []
T = 1/252
for i in range(0, trials):
    d_asian.append(S * growth(r,q,sigma,T))
    
df_asian = pd.DataFrame(d_asian)

df_asian = df_asian.rename(columns = {df_asian.columns[0] : 'Day1'})

for i in range(1,21):
    df_asian['Day' + str(i+1)] = 0
    for j in range(0, trials):
        df_asian.iloc[j,i] = df_asian.iloc[j,i-1]*growth(r, q, sigma, T)
        
df_asian['S_ave'] = df_asian.mean(axis=1)

put_asian = []
for s in df_asian['S_ave']:
    put_asian.append(max(0,K-s))
    
df_asian['put'] = put_asian

T = 1/12

put_price_asian = df_asian['put'].mean()*exp(-r*T)
se_asian = df_asian['put'].std() / sqrt(trials)

print(f' Asian Put option price = {put_price_asian*size}')
print(f'  95% Confidence = [{(put_price_asian - 1.965*se_asian)*size}, {(put_price_asian + 1.965*se_asian)*size}]')
