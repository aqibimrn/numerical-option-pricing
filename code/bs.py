# code/bs.py

## import libraries
import numpy as np
from scipy.stats import norm

## estimates current day price of a call option
## Black-Scholes price for a european call option
def bs_price_call(S, K, r, sigma, T):
    ### if time to maturity is zero or negative
    if T <= 0:
        return max(S - K, 0.0)
    
    ### compute d1 from the Black-Scholes formula
    ### np.log(S / K): log of spot price over strike price
    ### (r + 0.5 * sigma^2): risk-free growth rate adjusted for volatility
    ### T: time to maturity
    ### sigma * sqrt(T): volatility scaled by time
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

    ### compute d2, which is d1 minus volatility over sqrt(T)
    d2 = d1 - sigma * np.sqrt(T)

    ### Black-Scholes call price formula:
    ### S * N(d1): expected value of the stock payoff
    ### K * exp(-r * T) * N(d2): present value of paying the strike
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

    return float(price)

## Black-Scholes delta for a European call option
def bs_delta_call(S, K, r, sigma, T):
    if T <= 0:
        return 1.0 if S > K else 0.0
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

    return float(norm.cdf(d1))
