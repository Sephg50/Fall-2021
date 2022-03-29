# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 16:56:51 2021

@author: seph
"""

### Option Pricing with Black-Scholes-Merton Model ###

from math import log, sqrt, exp
from scipy.stats import norm

S = 19
K = 20   
T = 3/12
r = 0.04
"""r = DOMESTIC exchange rate"""
q = 0
""" q = FOREIGN exchange rate """
# known_q = 3
# known_q_T = 3/12
sigma = .4

def d1(S,K,T,r,q,sigma):
    return(log(S/K)+((r-q)+sigma**2/2)*T)/(sigma*sqrt(T))
def d2(S,K,T,r,q,sigma):
    return d1(S,K,T,r,q,sigma)-sigma*sqrt(T)
def bs_call(S,K,T,r,q,sigma):
    return S*exp(-q*T)*norm.cdf(d1(S,K,T,r,q,sigma))-K*exp(-r*T)*norm.cdf(d2(S,K,T,r,q,sigma))
def bs_put(S,K,T,r,q,sigma):
    return K*exp(-r*T)-S*exp(-q*T)+bs_call(S,K,T,r,q,sigma)

print(f'BSM Results: \n Spot Price = {S} \n Strike Price = {K} \n T = {T} \n r = {r} \n Dividend = {q} \n sigma = {sigma} \n ---------------')
print(f' d1 = {d1(S,K,T,r,q,sigma)}')
print(f' d2 = {d2(S,K,T,r,q,sigma)}')
print(f' call price = {bs_call(S,K,T,r,q,sigma)}')
print(f' put price = {bs_put(S,K,T,r,q,sigma)} ')


    
