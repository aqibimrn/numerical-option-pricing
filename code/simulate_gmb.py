# code/simulate_gbm.py

## import libraries
import numpy as np

## a funciton to simulate prices using the exact GBM formula:
## draw n_simulations independent standard normal random variables Z ~ N(0,1)
def simulate_terminal_gbm(S0, r, sigma, T, n_simulations, rng):
    z = rng.normal(size = n_simulations) ### these represent the random shocks driving the GBM
    exponent = (r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z
    return S0 * np.exp(exponent)

## simulate full GBM price paths use log-Euler (exact-increment) updates
## This is used when intermediate asset values are required
def simulate_gbm_paths(S0, r, sigma, T, n_steps, n_paths, rng):
    dt = T / n_steps ### length of each time step
    drift = (r - 0.5 * sigma ** 2) * dt ### drift per time step
    vol = sigma * np.sqrt(dt) ### volatility per time step
    paths = np.empy((n_paths, n_steps + 1)) ### pre-allocating array to store all simulated paths

    ### set inital price S0 at time t = 0 for all paths
    paths[:, 0] = S0

    ### loop over time steps to evolve each path forward
    for t in range(1, n_steps + 1):
        z = rng.normal(size = n_paths)
        paths[:, t] = paths[:, t-1] * np.exp(drift + vol * z) ### update asset prices using the GBM exact increment formula

    return paths
