# Numerical Option Pricing via Monte Carlo Simulation: Accuracy and Variance Reduction

## Project overview
This project explores how a stock price can evolve over time under simple random daily changes, using simulation to visualise and quantify the range of possible outcomes.
We implement two experiments:

1. **Single path simulation**: one representative price path over 100 days (visualises day-to-day randomness).
2. **Monte Carlo pricing of a European call**: simulate many independent price paths to estimate the option price and compare Monte Carlo estimators against the Black–Scholes analytic benchmark.

The primary goal is to show that Monte Carlo methods converge to the theoretical price and to demonstrate how variance-reduction techniques decrease estimator uncertainty.

## Repo Structure
option-pricing-mc/
├── code/
│   └──plots/
│       ├── single_price_path.png
│       ├── convergence_loglog.png
│       └── var_reduction_comparison.png
│   ├── simulate_gbm.py
│   ├── bs.py
│   ├── mc_pricing.py
│   ├── utils.py
│   └── experiments.py
├── README.md
├── requirements.txt
└── journal.md

## Modeling approach (method)
- **Model**: Geometric Brownian Motion (GBM) for the underlying stock price. GBM is chosen because it yields the Black–Scholes closed form which we use as a benchmark.
- **Initial price**: $100
- **Risk-free rate**: r = 1% (0.01)
- **Volatility (example)**: σ = 20% (0.2)
- **Option**: European call with strike K = 100, maturity T = 1.0 (1 year)
- **Monte Carlo**: simulate the terminal price S_T via the exact GBM terminal formula.
- **Estimators**:
    - Naive Monte Carlo (baseline)
    - Antithetic variates (pair Z and −Z)
    - Control variate (the terminal stock price discounted at the risk-free rate, with known expectation).

Important numerical parameters used for the reported experiments:
    - num_simulations = 10,000 for method comparison
    - Convergence experiments used n ∈ {1,000; 5,000; 10,000; 50,000}

Tools used: Python, NumPy, SciPy, Matplotlib, pandas.

## How to run (reproduce the plot & CSVs)
1. Install dependencies: pip install -r requirements.txt
2. Run the experiments script (creates plots in plots/ and CSVs in results/): python code/experiments.py
3. To rerun with different seeds or n values, edit code/experiments.py or invoke the functions inside with different arguments. 

- For reproducibility set np.random.default_rng(seed) with a fixed seed.

## Results
### Black–Scholes reference (call price)
**BS price:** 8.433319

### Monte Carlo estimates (S0=100, K=100, r=1%, σ=20%, T=1.0, n=10,000)
- **Naive MC:** 8.51049, **stderr** = 0.133503
- **Antithetic variates:** price = 8.489893, stderr = 0.10496
- **Control variate:** price = 8.355585, stderr = 0.059297
    - **Variance reduction factor (control vs naive)** ≈ 5.13

## Convergence results (naive MC)
Plots saved:
    - code/plots/convergence_loglog.png: absolute error vs number of simulations (log-log). The slope is ≈ −0.5, confirming convergence.
    - code/plots/var_reduction_comparison.png: bar chart showing standard error by method (n = 10,000).

(See code/results/var_reduction_comparison.csv for the numeric table of the comparison.)

## Interpretation
- **Convergence validated:** The Monte Carlo estimate steadily approaches the Black–Scholes price as the number of simulations increases. By n = 50,000, the absolute error is about 0.008, which means the result is effectively converged for practical purposes.

- **Variance reduction works:** Using antithetic variates slightly reduces the standard error.
The control variate method is much more powerful: the standard error drops from about 0.1335 to 0.0593, which is a variance reduction factor of roughly 5. In practical terms, this means you need about five times fewer simulations to reach the same level of accuracy.

- **There is no sign of bias:** all Monte Carlo estimates are close to the true (analytic) value, and the differences get smaller as the sample size increases. The variance-reduction methods also do not introduce any bias in this case.

## Limitations
This project deliberately uses a very simple model for teaching purposes:

- **The Geometric Brownian Motion (GBM) model** assumes that volatility is constant and that returns follow a lognormal distribution. In real financial markets, volatility tends to change over time and extreme price movements happen more often than this model allows.

- The control variate used here works well for European options under the GBM framework. If we use more complex models or different types of option payoffs, we would need other control techniques.

- These experiments also ignore real-world factors such as transaction costs, market liquidity, and the process of fitting the model to actual market data.

I would say these are opportunities for Level-2 upgrades (calibration to historical data, hedging P&L simulation, GARCH volatility, path-dependent payoffs).

## Reproducibility notes
- To reproduce the exact numbers reported, run code/experiments.py using the default random seeds specified in the script. Results may vary slightly across different seeds; for final results, we recommend running multiple seeds and reporting the average.

- All key outputs are saved as CSV files in code/results/, and generated plots are stored in code/plots/. A requirements.txt file is included in the repository to ensure reproducibility with exact package versions.

## Author

This project was completed as an implemented to build numerical intuition for quantitative finance and to prepare for supervised research opportunities.
