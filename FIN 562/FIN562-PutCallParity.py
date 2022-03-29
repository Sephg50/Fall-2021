# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 15:30:29 2021

@author: seph
"""

### Option pricing with put-call parity calculator ###

from math import exp

S = 19 - 2*exp(-0.04*(2/12))
K = 20
r = .04
q = 0
T = 3/12

# c = 1
# def put_option(S,K,r,q,T,c):
#     return c+(K*exp(-r*T))-(S*exp(-q*T))
# print(f'put option price = {put_option(S,K,r,q,T,c)}')

p = 5
def call_option(S,K,r,q,T,p):
    return p+(S*exp(-q*T))-(K*exp(-r*T))
print(f'call option price = {call_option(S,K,r,q,T,p)}')

print(2*exp(-0.04*(2/12)))



    
