# code/experiments.py

# Import libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from utils import compute_stderr, save_results_table, time_it
from mc_pricing import (mc_price_option_naive, mc_price_option_antithetic, mc_price_option_control_variate)
from bs import bs_price_call

# EXPERIMENT 1: CONVERGENCE OF NAIVE MONTE CARLO ESTIMATOR

def run_convergence_experiment(S0 = 100, K = 100, r = 0.01, sigma = 0.2, T = 1.0, seeds = 0):
    rng = np.random.default_rng(seeds) ## Create a random number generator with a fixed seed
    ns = [1000, 5000, 10000, 50000] ## Different Monte Carlo sample sizes to test convergence
    records = [] ## Store results for later analysis
    bs = bs_price_call(S0, K, r, sigma, T)
    
    ## loop over simulation sizes
    for n in ns:
        price, stderr, _ = mc_price_option_naive(S0, K, r, sigma, T, n, rng)

        ### record results
        records.append({
            "method": "naive",
            "n": n, 
            "price": price, 
            "stderr": stderr, 
            "abs_err": abs(price - bs)})
        
    df = pd.DataFrame(records) ## convert results to a dataframe

    df.to_csv("results/convergence_naive.csv", index=False) ## save numerical results to CSV

    ## PLOT CONVERGENCE

    plt.figure()
    plt.loglog(df["n"], df["abs_err"], marker='o')
    plt.xlabel("Number of simulations (n)")
    plt.ylabel("|MC - BS| (absolute error)")
    plt.title("Convergence: Naive MC absolute error vs n")
    plt.grid(True)

    # Save plot to disk
    plt.savefig("plots/convergence_loglog.png", dpi=200)
    plt.close()

    ## confirmation message
    print("Saved plots/convergence_loglog.png and results/convergence_naive.csv")

    return df

# EXPERIMENT 2: VARIANCE REDUCTION METHOD COMPARISON

# Compares naive Monte Carlo, antithetic variates, and control variate methods using same number of simulations
# Reports option price estimates, standard errors, and variance reduction factors
def run_variance_reduction_comparision(S0 = 100, K = 100, r = 0.01, sigma = 0.2, T = 1.0, n = 10000, seed = 0):
    rng = np.random.default_rng(seed) ## initialize random number generator

    p_naive, se_naive, samples_naive = mc_price_option_naive(S0, K, r, sigma, T, n, rng) ## naive monte carlo pricing
    p_anti, se_anti, samples_anti = mc_price_option_antithetic(S0, K, r, sigma, T, n, rng) ## antithetic variates monte carlo

    p_cv, se_cv, var_red, samples_cv = mc_price_option_control_variate(S0, K, r, sigma, T, n, rng) ## control variate monte carlo

    bs = bs_price_call(S0, K, r, sigma, T) ## black scholes ref

    ## save numerical comparison
    df = pd.DataFrame([{"method": "BS", "price": bs, "stderr": 0.0}, {"method": "naive", "price": p_naive, "stderr": se_naive}, {"method": "antithetic", "price": p_anti, "stderr": se_anti}, {"method": "control_variate", "price": p_cv, "stderr": se_cv, "var_reduction": var_red}])

    df.to_csv("results/var_reduction_comparision.csv", index = False) ## save results to CSV

    ## plot standard errors
    methods = df["method"]
    stderr = df["stderr"].fillna(0.0)

    plt.figure(figsize=(6, 4))
    plt.bar(methods, stderr)
    plt.ylabel("Standard error of estimator")
    plt.title(f"Estimator stderr by method (n={n})")

    ## save plot
    plt.savefig("plots/var_reduction_comparison.png", dpi=200)
    plt.close()

    print("Saved plots/var_reduction_comparison.png and results/var_reduction_comparison.csv")
    return df

# Run experiments when file is executed directly

if __name__ == "__main__":
    run_convergence_experiment() ## run study for naive monte carlo
    run_variance_reduction_comparision() ## run variance reduction comparison