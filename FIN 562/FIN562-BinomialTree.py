#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 14:13:24 2021

@author: seph
"""

from math import log, sqrt, pi, exp

# Binomial Tree Calculator with variable inputs

S = 40
K = 40
r = 0.04
"""r = DOMESTIC exchange rate"""

T = 0.5
sigma = 0.3

q = 0
""" q = FOREIGN exchange rate """

steps = 1

u = exp(sigma*sqrt(T))
d = 1/u

# u = 22/20
# d = 18/20
"""if u and d are given"""

p = (exp((r-q)*T) - d)/(u-d)

# p = (1 - d)/(u-d)
"""for futures"""

print(f' Binomial tree with {steps} step(s): \n Spot Price = {S} \n Strike Price = {K} \n r = {r} \n T = {T} \n sigma = {sigma} \n dividend = {q} \n -----------------')

if steps == 1:
    Su = S * u
    Sd = S * d

    Fu_put = max(0, K - Su)
    Fd_put = max(0, K - Sd)

    Fu_call = max(0, Su - K)
    Fd_call = max(0, Sd - K)

    F_put = (p*Fu_put+(1-p)*Fd_put)*exp(-r*T)
    F_call = (p*Fu_call+(1-p)*Fd_call)*exp(-r*T)

    print(f' Put option price = {F_put}')
    print(f' Call option price = {F_call}')
    
elif steps == 2:
    Suu = S * u ** 2
    Sud = S * u * d
    Sdu = S * d * u
    Sdd = S * d ** 2
    
    Fuu_put = max(0, K - Suu)
    Fud_put = max(0, K - Sud)
    Fdu_put = max(0, K - Sdu)
    Fdd_put = max(0, K - Sdd)
    
    Fuu_call = max(0, Suu - K)
    Fud_call = max(0, Sud - K)      
    Fdu_call = max(0, Sdu - K)
    Fdd_call = max(0, Sdd - K)
    
    Fu_put = (p * Fuu_put + (1-p) * Fud_put) * exp(-r*T)
    Fu_call = (p * Fuu_call + (1-p) * Fud_call) * exp(-r*T)
    
    Fd_put = (p * Fdu_put + (1-p) * Fdd_put) * exp(-r*T)
    Fd_call = (p * Fdu_call + (1-p) * Fdd_call) * exp(-r*T)
    
    F_put = (p * Fu_put + (1-p) * Fd_put) * exp(-r * T)
    F_call = (p * Fu_call + (1-p) * Fd_call) * exp(-r * T)
    
    print(f' Put option rice = {F_put}')
    print(f' Call option price = {F_call}')
    
elif steps == 3:
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
    
    Fuuu_call = max(0, Suuu - K)
    Fuud_call = max(0, Suud - K)
    Fudu_call = max(0, Sudu - K)
    Fudd_call = max(0, Sudd - K)    
    Fduu_call = max(0, Sduu - K)
    Fdud_call = max(0, Sdud - K)
    Fddu_call = max(0, Sddu - K)
    Fddd_call = max(0, Sddd - K)   
    
    Fuu_put = (p * Fuuu_put + (1-p) * Fuud_put) * exp(-r*T)
    Fud_put = (p * Fudu_put + (1-p) * Fudd_put) * exp(-r*T)
    Fdu_put = (p * Fduu_put + (1-p) * Fdud_put) * exp(-r*T)
    Fdd_put = (p * Fddu_put + (1-p) * Fddd_put) * exp(-r*T)
    
    Fuu_call = (p * Fuuu_call + (1-p) * Fuud_call) * exp(-r*T)
    Fud_call = (p * Fudu_call + (1-p) * Fudd_call) * exp(-r*T)
    Fdu_call = (p * Fduu_call + (1-p) * Fdud_call) * exp(-r*T)
    Fdd_call = (p * Fddu_call + (1-p) * Fddd_call) * exp(-r*T)
    
    Fu_put = (p * Fuu_put + (1-p) * Fud_put) * exp(-r*T)
    Fu_call = (p * Fuu_call + (1-p) * Fud_call) * exp(-r*T)
    
    Fd_put = (p * Fdu_put + (1-p) * Fdd_put) * exp(-r*T)
    Fd_call = (p * Fdu_call + (1-p) * Fdd_call) * exp(-r*T)
    
    F_put = (p * Fu_put + (1-p) * Fd_put) * exp(-r * T)
    F_call = (p * Fu_call + (1-p) * Fd_call) * exp(-r * T)
    
    print(f' Put option rice = {F_put}')
    print(f' Call option price = {F_call}')
