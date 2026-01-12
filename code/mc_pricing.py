# code/mc_pricing.py

# Import libraries
import numpy as np
from simulate_gmb import simulate_terminal_gbm
from utils import compute_stderr

# Function for computing the payoff of a European call options
def payoff_call(ST, K):
    return np.maximum(ST - K, 0.0)

# Naive Monte Carlo pricing of a European call option
# Function simulates terminal prices and averages discounted payoffs
def mc_price_option_naive(S0, K, r, sigma, T, n_simulations, rng):
    ST = simulate_terminal_gbm(S0, r, sigma, T, n_simulations, rng)
    payoffs = np.exp(-r * T) * payoff_call(ST, K)
    price = payoffs.mean()
    stderr = compute_stderr(payoffs)
    return float(price), float(stderr), payoffs

# Monte Carlo pricing using antithetic variates
# Uses paired normal draws (Z, -Z) to reduce variance
def mc_price_option_antithetic(S0, K, r, sigma, T, n_simulations, rng):
    half = n_simulations // 2
    z = rng.normal(size = half) ## sample std normal random variables

    exponent1 = (r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z
    exponent2 = (r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * (-z)

    ST1 = S0 * np.exp(exponent1)
    ST2 = S0 * np.exp(exponent2)
    ## Average the paired discounted payoffs
    payoffs = 0.5 * (np.exp(-r * T) * np.maximum(ST1 - K, 0.0) + np.exp(-r * T) * np.maximum(ST2 - K, 0.0))

    ## Antithetic Monte Carlo price estimate
    price = payoffs.mean()

    ## Standard error of the estimate
    stderr = compute_stderr(payoffs)

    return float(price), float(stderr), payoffs

# Monte Carlo pricing using a control variate
def mc_price_option_control_variate(S0, K, r, sigma, T, n_simulations, rng):
    ST = simulate_terminal_gbm(S0, r, sigma, T, n_simulations, rng)

    discount = np.exp(-r * T) ## Discount factor

    Y = discount * np.maximum(ST - K, 0.0)
    X = discount * ST
    
    EY = Y.mean() ## Sample mean of payoff
    EX = X.mean() ## Sample mean of control variate

    cov = np.cov(Y, X, ddof = 1)[0, 1]
    varX = np.var(X, ddof = 1) ## Sample variance of control variate

    if varX == 0: ## Prevent error of division of 0
        beta = 0.0
    else:
        beta = cov / varX
    
    Y_adj = Y - beta * (X - S0) 
    price_adj = Y_adj.mean() 
    stderr_adj = compute_stderr(Y_adj) ## standard error of adjusted estimator

    var_naive = np.var(Y, ddof = 1)
    var_adj = np.var(Y_adj, ddof = 1)

## variance reduction factor
    if var_adj > 0:
        var_reduction = float(var_naive / var_adj)
    else:
        var_reduction = float('inf')
    
    return float(price_adj), float(stderr_adj), float(var_reduction), Y_adj
