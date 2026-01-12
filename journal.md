DAY 1
=====

While exploring financial mathematics on YouTube, I came across the Black–Scholes model for option pricing. It reminded me of a previous project I had done using Monte Carlo simulation, which sparked an idea: I could combine these two approaches by using Black–Scholes as a benchmark to evaluate and improve Monte Carlo pricing. This project grew out of that curiosity, aiming to study how variance-reduction techniques can make Monte Carlo simulations more accurate and efficient, while comparing the results against the analytical Black–Scholes solution.
Essentially, I am trying to compute the expected discounted payoff of an option when the stock price is random. This project aims to be a computational finance project where I price options using Monte Carlo simulation, validate against Black–Scholes, and increse my knowledge in variance reduction.

DAY 2
=====

I am now getting started on my project, I will create a utility file for my utility functions, such as a calculator for standard error (to calcualte and report uncertainity), a time wrapper (so I can report the CPU ) and a save results function.
I have set it so the code would add the results into the results folder in code directory.

DAY 3
=====

Next, I am now going to create simulate_gbm.py, and simulate_terminal_gbm & simulate_gbm_paths functions. The purpose for these functions is to create realistic stock price simulations, either by jumping straight to the final price or by showing how the price evolves over time. The goal is to keep the simulations simple, fast, and flexible for different financial scenarios.
I have now created the functions.

DAY 4
=====

I am now creating bs.py, the brains behind the Black-Scholes model. This file would implement the Black–Scholes model to price European call options and compute their delta, measuring how the option’s value changes with respect to the underlying asset price under risk-neutral assumptions.
This was relatively straight forward to code, and is now complete.

DAY 5
=====

Today I implemented Monte Carlo pricing for a European call option. I started with a naive Monte Carlo estimator, then extended it using variance-reduction techniques. For each method, I computed both the option price and the standard error to quantify uncertainty. 
This sets up a direct comparison of efficiency and accuracy against the Black–Scholes benchmark, and highlights how variance reduction can significantly improve Monte Carlo performance.

DAY 6
=====
Today I wrote the experimental framework for the project. I created experiments.py to run convergence tests for the naive Monte Carlo estimator and to compare variance-reduction methods (naive, antithetic, and control variates) against the Black–Scholes price.

The experiments automatically save numerical results and generate plots showing convergence behavior and standard error reduction. This makes it easy to empirically verify Monte Carlo convergence and clearly see the efficiency gains from variance reduction.
This is now complete!